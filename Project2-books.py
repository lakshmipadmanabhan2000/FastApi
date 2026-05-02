from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
app=FastAPI()

class Book:
    id: int
    title: str
    description:str
    author: str
    rating: int
    published_date: int
    def __init__(self,id,title,description,author,rating,published_date):
        self.id=id
        self.title=title
        self.description=description
        self.author=author
        self.rating=rating
        self.published_date=published_date

#validating request body
class BookRequest(BaseModel):
    id: Optional[int]= Field(description='Id not required on Create',default=None)
    title: str = Field(min_length=3)
    description:str =Field(min_length=1,max_length=100)
    author: str =Field(min_length=1)
    rating: int =Field(gt=0,lt=6) # b/w 1 and 5
    published_date: int=Field(gt=1990,lt=2030)

    #example payload
    model_config={
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "description": "New description",
                "author": "New author",
                "rating": 5,
                "published_date":"2010"
            }
        }
    }

BOOKS=[
    Book(1,'Book 1','First book','Author 1',4,2012),
    Book(2,'Book 2','Second book','Author 2',2,2023),
    Book(3,'Book 3','Third book','Author 3',3,2002),
    Book(4,'Book 4','Fourth book','Author 4',5,2012),
    Book(5,'Book 5','Fifth book','Author 5',3,2000),
    Book(6,'Book 6','Sixth book','Author 6',3.7,2026)
    ]
#read all books
@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

#create new book
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(new_bookRequest: BookRequest):
    new_book=Book(**new_bookRequest.model_dump())
    b=find_book_id(new_book)
    BOOKS.append(b)

#generate id (1 more than last)
def find_book_id(book:Book):
    book.id=1 if len(BOOKS)==0 else BOOKS[-1].id+1
    return book

#get book by id
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def find_book_by_id(book_id:int =Path(gt=0)):
    for book in BOOKS:
        if(book.id==book_id):
            return book
    raise HTTPException(status_code=404, detail="Book Not Found!")

#get book by rating    
@app.get("/books/",status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(gt=0,lt=6)):
    return_list=[]
    for book in BOOKS:
        if(book.rating==rating):
            return_list.append(book)
    return return_list

#update book, modify response status code
@app.put("/books/",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    is_Updated=False
    for i in range(len(BOOKS)):
        if(BOOKS[i].id==book.id):
            BOOKS[i]=book
            is_Updated=True
    #raise exception if book not found
    if not is_Updated:
        raise HTTPException(status_code=404, detail="Not found!")
    
#delete book, validate Path parameter
@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int =Path(gt=0)):
    is_Deleted=False
    for i in range(len(BOOKS)):
        if(BOOKS[i].id==book_id):
            BOOKS.pop(i)
            is_Deleted=True
            break
    if not is_Deleted:
        raise HTTPException(status_code=404,detail="Not Found!")
    
#get book by published year, validate query parameter
@app.get("/books/publish/",status_code=status.HTTP_200_OK)
async def get_books_by_publishedDate(year:int =Query(gt=1990,lt=2030)):
    book_list=[]
    for b in BOOKS:
        if(b.published_date==year):
            book_list.append(b)
    return book_list

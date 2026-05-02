from fastapi import FastAPI,Body

app=FastAPI()

@app.get('/api-endpoint')
async def welcome_message():
    return {'message':'Hello World !'}

BOOKS=[{'Title':'Title 1','Author':'Author 1','Category':'Maths'},
       {'Title':'Title 2','Author':'Author 2','Category':'English'},
       {'Title':'Title 3','Author':'Author 3','Category':'Science'},
       {'Title':'Title 4','Author':'Author 2','Category':'Science'},
       {'Title':'Title 5','Author':'Author 4','Category':'English'},
       {'Title':'Title 6','Author':'Author 2','Category':'Science'}

       ]
@app.get('/books')
async def read_all_books():
    return BOOKS

@app.get('/books/mybook')
async def read_all_books():
    return {'book_title':'My Favorite Book'}

#path parameter
@app.get('/books/{book_title}')
async def read_book(book_title:str):
    for book in BOOKS:
        if(book.get('Title').casefold()==book_title.casefold()):
            return book
# @app.get('/books/mybook')
# async def read_all_books():
#     return {'book_title':'My Favorite Book'}

#query parameter
@app.get("/books/")
async def read_book_by_category(category:str):
    return_list=[]
    for book in BOOKS:
        if(book.get('Category').casefold()==category.casefold()):
            return_list.append(book)
    return return_list

#create book
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return "Book Created Successfully !"

#update book
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if(BOOKS[i].get('Title').casefold()==updated_book.get('Title').casefold()):
            BOOKS[i]=updated_book

#delete book
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    #approach 1
    for i in range(len(BOOKS)):
        if(BOOKS[i].get('Title').casefold()==book_title.casefold()):
            BOOKS.pop(i)
            break
    #approach 2
    #for book in BOOKS:
    #    if(book.get('Title').casefold()==book_title.casefold()):
    #        BOOKS.remove(book)
    #       break

#Get all books of a specific author by path parameter
@app.get("/books/get_books_of_an_author/{author_name}")
async def get_books_of_an_author(author_name:str):
    book_list=[]
    for book in BOOKS:
        if(book.get('Author').casefold()==author_name.casefold()):
            book_list.append(book)
    return book_list

#Get all books of a specific author by query parameter
@app.get("/books/get_books_of_an_author/")
async def get_books_of_an_author(author_name:str):
    book_list=[]
    for book in BOOKS:
        if(book.get('Author').casefold()==author_name.casefold()):
            book_list.append(book)
    return book_list

#query and path parameter together
@app.get("/books/{author_name}/")
async def read_book_by_author_and_category(author_name:str,category: str):
    return_list=[]
    for book in BOOKS:
        if(book.get('Author').casefold()==author_name.casefold() 
           and 
           book.get('Category').casefold()==category.casefold()
           ):
            return_list.append(book)
    return return_list
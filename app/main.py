from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):    #to define the structure of application
    title: str
    content: str
    published: bool = True   
    rating: Optional[int] = None
#title str, content str,category, bool published





my_posts =[{"title":"title of post 1","content":"content of post1","id":1},{"title":"Favorite foods","content":"I like pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

        
        


# request Get method url "/
@app.get("/")     #This is we called as decoraters
def root():
    return {"message": "This is KK and FastAPI is OP"}



@app.get("/posts")    #decoraters
def get_posts():
    return {"data": my_posts}



@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/recent/latest")  # this function is just for understanding the inportance of path parameter issues

def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}


@app.get("/posts/{id}")  # here {id} => is called as path parameter (basically returns the id)
def get_post(id:int,response:Response):    # to pass the message for non integer types (data validation)
    post = find_post(int(id))  # because in my_posts dictionary it is returning string so we have to type cast of we can use pydantic fucntionality in after the passing the function it while we are returning from that 
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail =f"Unfortunaterly it's not available with id {id}!")

        # response.status_code = status.HTTP_404_NOT_FOUND 
        # return {"message":f"Sorry it's not avaliable with id {id}"}
   
    return {"post_detail":post}


#Always remember and be careful with path parameter variables as they can mismatch and may give you an issue
#So fot that fastapi works with top down priority basis ,so whenever you are just specifying the path just specify on top of it (which ever you want to give priority)
# or we can add the latest into the new path to avoid such type of issues

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting post
    #find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_post(id:int, post:Post):
    
    index = find_index_post(id)

    if index ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f'post with :{id} does not exist')
    
    post_dict = post.dict()
    post_dict['id'] =id
    my_posts[index] = post_dict
    return {'data': post_dict}


    #now from now onwards we will work with database








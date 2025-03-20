# ReadMe

I will be going through my lessons from playing around with docker and keras to create this. 

Credit to [Beyond Fireship](https://www.youtube.com/watch?v=cw34KMPSt4k) which i used as a starting point for the flask server and webpage.

## Docker

Dockerfile is a file that contains the instructions for docker to execute. I used a slim version of python as the base image and played around with it while trying to get my dependencies to work. If i were to do this again, I'd probably use the tensorflow base image so i dont need to deal with as many dependencies. 

`docker build . -t mnist` builds the image

I have it currently configured to use the local machine port 1313 for everything. 

So if you are running the docker container you'll need to bind 
the port to 1313 with `docker run -d -p 8080:5100 mnist`

I set up the docker-compose.yml to handle that. `docker-compose up -d` will do all the setup needed (asuming you've already built the image)

TLDR
```
docker build . -t mnist
docker-compose up -d
```

## Models
The models are trained in [google colab](https://colab.research.google.com/drive/1gmunFtzOIbfsgIB-YCj04Slyv2LS5Ri2?usp=sharing)

## Key takeaways
This was as much a learning opportunity in docker as it was in machine learning. A few key lessons I learned were:
- Normalization
- Data Augmentation (adding inverted images)
    - Before changing a lot of backend logic, i used to preprocess imgs and return a copy of the inverted img and check if that img was classified better
    - by training on these inverted imgs I simplify the code on backend
- CNN
    - adding convolutions can help determine basic features
    - max pooling can help get rid of noise and help the model pay attention to areas with high feature detection
    - adding more conv layers can help detect more detailed features
- batch normalization
    - helps stabalize activations (outputs from one layer to the next) by normalizing them before scaling them. Can help when the input to the batch norm layer can vary a lot. 
- Custom activation functions
    - i used abs value as a lambda because i think that the original CNN model was learning pairs of features. One for regular images and one for inverted but they would be the same feature (ie. vertical edges). 
    - By using abs value, any kernel would produce the same output regardless of color inversion. 
- Dropout
    - Added this to avoid overfitting

Through this, I achieved >99% accuracy on the test data.
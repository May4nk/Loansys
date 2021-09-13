# Loansys

A loan system with role(admin,agent,user) restriction api in django rest framework

To run this file download docker-compose,
run docker-compose build then docker-compose up,                                                                       
It will automatically install requirement in container and run it.                                                                                  

# Usage

(:pk = primary key)

****Allowed any****

To register a user send POST request to /register/

****To get authentications token****

To get authentication token after registration send POST request to /login/                                                                    

****User can be viewed,updated,deleted by only Admin role****

To view all users send GET request to /users/                                                                   
To view one user send GET request to /user/pk/                                                
To update user send PUT request to /user/pk/                                         
To delete user send DELETE request to /user/pk/                                                               
  
****An Agent can make request for loan and view his all customer and A customer can view his only requests****

To view his own request send GET request to /request/pk/                                                                            
To make a request send POST request to /requests/                                                                                    
  
****A request can be deleted and updated and viewed all by Admin only****
 
To view all requests send GET request to /requests/                                                                                    
To delete request send DELETE request to /request/pk/                                                                              
To update request send PUT request to /request/pk/                                                                           

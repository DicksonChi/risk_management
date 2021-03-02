#  Risk Management Coding Test
* [Dependencies](#dependencies)
* [Test Description and Approach](#test-description-and-approach)
* [Installation](#installation)
* [Running Locally](#running)
* [Testing](#testing)
* [Linting](#testing)
* [Deployment](#deployment)

## Dependencies

This project makes use of these dependencies:

* Python 3.8 - Programming language for backend development
* Django REST framework - REST API
* VueJs for the frontend development
* AWS LAMBDA and s3 bucket
* Postgres RDS
* Zappa for deployment


## Test Description and Approach
This is a Single Page Application created with VueJs and consumes a REST API created with Django
to show the list of risk types, and the list of fields.  

This solution can allow for usage by different users without using 
authentication but just a simple id that is saved on their browser once 
the user enters an email.

* If the user has not used the application before it registers them with
that email. If the email has already been used before it continue with that email the
next time.
  
* The users can add many Risk Type and also add any field to the list of already existing fields

## Installation
```
$ git clone git@github.com:DicksonChi/risk_management.git
$ cd risk_management
$ virtualenv -p /usr/bin/python3.8 virtualenv
$ source virtualenv/bin/activate
```


##### TO INSTALL DEPENDENCIES FOR THE BACKEND
`$ make requirements_dev`

##### TO INSTALL DEPENDENCIES FOR THE FRONTEND
`$ make install-fd`

## Running

##### TO RUN BACKEND
`$ make migrate`
 
`$ make run`
 
`$ make superuser` to create superuser


##### TO RUN FRONTEND
`$ make serve `


## Testing

`$ make test`

 *This command runs the `pytest` command and then creates coverage report when run.* 

##### cleanup after testing
`$ make clean`

 *after running the test there might be `.pyc ` or `__pycache__` files
so this command runs through all directories and cleans up.*


## Linting
##### Linting and static analysis backend
`$ make lint_backend`

*This command checks for the PEP issues with the python code and uses 
the `prospector.yml` defined conditions and using pylint to also check 
for linting issues in the python code and alerts you to conform to the standard.*

##### Linting and static analysis frontend
`$ make lint_frontend`

*The command runs the `npm run lint` command to apply linting
and fixes to your Vue.js code*


## Deployment

##### Backend Deployment
run this command

  ` $ make backend_deploy_start`

Provide default settings to your zappa_settings.json file:

```
- Name of environment - just accept the default 'dev'
- S3 bucket for deployments - just accept the default
- Zappa should automatically find the correct Django settings file so accept the default
```

Update the settings file in risk_management/risk_management and add zappa_django_utils in the list of apps

Go to your AWS console and create the VPC and then the RDS 

Make sure you link the VPC and Security groups to the RDS and also to the lambda function where the zipped project is hosted

Then update the zappa_settings.json file
```json
{
  "vpc_config": {
   "SubnetIds": [
    "your-subnet-1",
    "your-subnet-2",
    "your-subnet-3"
   ],
   "SecurityGroupIds": [
    "your-security-group"
   ]
  }
}
```

The whole zappa_setting.json should look like this
```json
{
    "dev": {
        "aws_region": "eu-west-3",
        "django_settings": "risk_management.settings",
        "profile_name": "default",
        "project_name": "risk-management",
        "runtime": "python3.8",
        "s3_bucket": "YOUR BUCKET NAME",
        "timeout_seconds": 900,
        "manage_roles": false,
        "role_name": "YOUR ROLE THAT HAS PERSMISSION", // created from aws with your IAM configuration
        "role_arn": "ROLE ARN",
        "vpc_config" : {
            "SubnetIds": ["your-subnet-1", "your-subnet-2", "your-subnet-3"],
            "SecurityGroupIds": [ "your-security-group" ]
        }
    }
}
```

Now run `$ make stage=YOUR_STAGE_NAME backend_deploy`
you should get this message 
  ```
  Scheduled risk-management-dev-zappa-keep-warm-handler.keep_warm_callback with expression rate(4 minutes)!
  Deploying..
  Your application is now live at https://URI.REGION.amazonaws.com/STAGE_NAME
  ```

Then run the command to update this deployment

   ```
     $ make stage=STAGE_NAME backend_update
   ```

Now lets create the db. Since we already have the VPC and the RDS setup
run this command
  ```
   $ make stage=STAGE_NAME backend_create_db
   ```
*note: please replace the STAGE_NAME with the stage name you want to deploy*

If you get the error message that a db with same name exists, then ignore
 Now let us migrate, load fixtures and create admin user
```
$ make stage=STAGE_NAME backend_migrate
$ make command="loaddata fixtures/default_category.json" backend_command
$ make command="from main.models import User; User.objects.create_superuser(email='admin@ybritecore.com', password='password')" backend_command
```

##### Frontend Deployment
After deploying the backend code get the endpoint URL and update the PROD constant in constants.js file in 
`frontend/src` 

create the s3 bucket that will collect the static files for the frontend.

Go to the bucket permission and then under the cors configuration copy this code to allow for public access
  ``` json
   {
  "Version":"2012-10-17",
  "Statement":[{
	"Sid":"PublicReadGetObject",
        "Effect":"Allow",
	  "Principal": "*",
      "Action":["s3:GetObject"],
      "Resource":["arn:aws:s3:::BUCKET-NAME-GOES-HERE/*"
      ]
    }
  ]
}
  ```

go to the properties page and specify that this bucket is for hosting a static website

run this command to then deploy the frontend

  `$ make bucket=s3://YOUR_BUCKET build_deploy`

Copy the url of the static bucket and access it from your browser.

Now you too can now make a list of your Risk Type with its custom fields!

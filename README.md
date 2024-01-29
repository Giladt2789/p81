<h1>Perimeter 81 home assignment</h1>
<h2>Main goals of assignment</h2>
1. Deploy infrastructure in AWS cloud using terragrunt for: <br>
    * Cloudfront <br>
    * S3 bucket <br>
With the following restrictions: <br>
<b><div align="center"><h3>Acces to the bucket should be allowed only from cloud front</b></div></h3>

2. Write a python code that will: <br>
2.1. Will download a JSON from https://dummyjson.com/products <br>
2.2. Will parse the downloaded JSON by going over all the “products” nodes in the file and find all products that there prices are >=100, <br>
save it to new JSON with expected results.
2.3. Upload the new JSON file to S3 bucket <br>
2.4. Download the JSON file via cloudfront url that was built in phase 1 and print if the file is of json format or not<br>

3. Write and Pack the pipeline in github actions, that will deploy your terragrunt project alongside the python code must be done in 2 seprated steps
(1 for infra and second for code).

<h2>My solution</h2><br>
In the process of solving this home assignment, i've made some assumptions and taken some steps:<br>
1. The bucket that would save the state file and the DynamoDB table that stores the LockID must get created via boto3 and not terraform. <br>
2. The entire process must be a plug-and-play process. So, the things i've made to support it are:<br>
2.A. The AWS access key and secret are stored in the Github credentials, in order for them not to be printed in the console, or stored in the git repo. <br>
2.B. In order to have the option to plug-and-play, input parameters are permitted in the <b>"Run workflow"</b> option under the Actions tab. <br>
2.C. The input parameters that will be passed are:<br>
    * Region - the AWS region to deploy the resources<br>
    * State_Files_Bucket - the buckets name to store the state files<br>
    * Profile_Name - in the AWS cli, i've used the profiles method to identify. For that reason, a name for that profile must be given.<br>
    * Statefile_Lock_Table - in order to track the lock status, a DynamoDB table must be created.<br>
    * Account_Number - the AWS account number (provided by Perimeter 81 team)<br>
    * IAM_User_Name - the IAM user name (provided by Perimeter 81 team)<br>
    * Task_Bucket_Name - the bucket name that will store the final json file<br>
    * Origin_id - a name for the origin id (i used it to define a name for the cloudfront origin)<br>
    * Action - this part is my overthinking:<br>
      * If i want to execture the assignment mission - i provide the keyword "create".<br> 
      * If i want to destroy the infrastructure, for whatever reason - i provide the keyword "destroy". <br>
<p align="center"><img src="https://github.com/Giladt2789/p81/assets/112761499/e9c075b6-c788-4343-9d73-7ed099527847" alt="Inputs"></p><br>


3. In order not to over-complex the task, i didn't used a self-hosted runner for github (it wasn't the assignment to create that machine).<br>
If i was to create that machine - many steps would have been avoided.<br>

The overall flow goes as such:<br>
First i'm creating (using boto3 SDK) the statefile bucket and dynamodb table for LockID <br>
Then i'm triggering the terragrunt action in order to deploy the infrastructure.<br>
Afterwards, i'm triggering my python code to filter, parse and upload the final json file to the deployed bucket. <br>
In the later step i'm also checking if the final json file (that was uploaded after parsing and downloaded as final_catalog) is indeed a json file or not (as requested in the task)<br>
If we'll choose to go via the destroy option - we'd be doing the following:<br>
First we'll empty the task bucket (in order to be able to remove the bucket using terragrunt. When a bucket has an object, even a version object - terragrunt can't delete that bucket)<br>
Second, we'll destroy the infrastructure using terragrunt.<br>
At the end, we'll remove the state file bucket and the dynamodb table using boto3 SDK. That will be the end of the destroy option.<br>
Hope you enjoyed reading and reviewing the task solution<br>

<h3>Resources and documentations i've used in the process</h3><br>
Github Actions Docs: https://docs.github.com/en/actions<br>
Boto3 docs: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html<br>
Terragrunt docs: https://terragrunt.gruntwork.io/docs/<br>
Terraform registry: https://registry.terraform.io/<br>
Github Actions Marketplace: https://github.com/marketplace?type=actions <br>

<h1>Perimeter 81 home assignment</h1>
<h2>Main goals of assignment</h2>
1. Deploy infrastructure in AWS cloud using terragrunt for: <br>
    * Cloudfront <br>
    * S3 bucket <br>
With the following restrictions: <br>
<b><div align="center"><h3>Acces to the bucket should be allowed only from cloud front</b></div></h3>

2. Write a python code that will: <br>
2.1. Will download a JSON from https://dummyjson.com/products
2.2. Will parse the downloaded JSON by going over all the “products” nodes in the file and find all products that there prices are >=100, <br>
save it to new JSON with expected results.
2.3. Upload the new JSON file to S3 bucket
2.4. Download the JSON file via cloudfront url that was built in phase 1 and print if the file is of json format or not

3. Write and Pack the pipeline in github actions, that will deploy your terragrunt project alongside the python code must be done in 2 seprated steps
(1 for infra and second for code).

<h2>My solution</h2><br>
In the process of solving this home assignment, i've made some assumptions and taken some steps:<br>
1. The bucket that would save the state file and the DynamoDB table that stores the LockID must get created via boto3 and not terraform. <br>
2. The entire process must be a plug-and-play process. So, the things i've made to support it are:<br>
2.1. The AWS access key and secret are stored in the Github credentials, in order for them not to be printed in the console, or stored in the git repo. <br>
2.2. In order to have the option to plug-and-play, input parameters are permitted in the <b>"Run workflow"</b> option under the Actions tab. <br>
2.3. The input parameters that will be passed are:<br>
    * 
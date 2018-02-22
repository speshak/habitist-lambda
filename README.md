# habitist-lambda

[![Maintainability](https://api.codeclimate.com/v1/badges/a98e3dca88b86d88fbcc/maintainability)](https://codeclimate.com/github/speshak/habitist-lambda/maintainability)

An [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html) implementation of
[amitness/habitist](https://github.com/amitness/habitist).  Unlike the
original, this uses a schedule to fire and therefore doesn't need the webhook
or IFTTT trigger.


## Usage

![Habitist Screenshot](https://i.imgur.com/q4h2QGv.png)

1. You add habits you want to form as task on todoist with schedule `every day`

2. Add `[day 0]` to the task

3. When you complete the task, the [day 0] will become [day 1]

4. If you fail to complete the task and it becomes overdue, the script will schedule it to today and reset [day X] to [day 0].



## Installation

1. Install [Serverless framework](https://serverless.com/) using their [install instructions](https://serverless.com/learn/quick-start/#installing-serverless)

2. Save your Todoist API key as an [SSM Parameter](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html)
    ```
    aws ssm put-parameter --name TodoistApiKey --type SecureString --value <your API key>
    ```

3. Deploy the function
    ```
    serverless deploy -s prod
    ```

4. (Optional) Test the function.
    ```
    serverless invoke -f habit_process
    ```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

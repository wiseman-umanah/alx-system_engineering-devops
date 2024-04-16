## WEB_STACK DEBUGGING 4

In this web_stack debugging, there's more of open file permission for multiple files.

# Task 0
We try to make 2000 requests to our web servers to see how our server will respond and handle them
In the process about 937 requests failed, which is not suppose to be so.
During the debugging stage, it was discovered that the issue was caused by limited access to responses.
It was quickly adjusted  and improved.

# Task 1
In this task, the user holberton cannot open multiple files
When the user is log in, an error message is displayed which is not what is expected
During debugging, the issue was seen as a bug in the OS configuration file
The open file option was adjusted to unlimite opening of files for holberton user

All task are solved and should work as expected in any use case.
The puppet files serve as automation files for similar issues.

![image](https://github.com/wiseman-umanah/alx-system_engineering-devops/assets/126745459/2eca2bc2-d4fe-406f-86a7-48ec9b87c7e4)


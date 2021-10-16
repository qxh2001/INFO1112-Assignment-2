<h1>INFO1112 Assignment: 2020S2</h1>
<h2>By Katherine Xu</h2>

<h3>Code: `webserv.py`</h3>
* In this file, I wrote all of the code for the assignment. 

* I only used one function to check the headers.

<h3>CGI script files: `cgibin`</h3>
* All of the CGI script files, including those in my test cases, are inside this folder.

* Although I'm not sure if we are supposed to read `.sh` files besides `.py` files, I wrote a test case in bash.

<h3>Extra Files for testing: `files`</h3>
* This folder includes the static pages.

* It also includes some images (Anime memes) for testing the content types!

<h3>Test Cases: `tests`</h3>
* All of the given test cases has been modified, starting with `staff`.

* I believe the names are self-explanatory, but this is an detailed explanation:

  * The test cases might have 2~3 files associated to it.
  
    * `.sh`: bash script to test the program
    
    * `.out`: expected output
    
    * `.cfg`: configuration file for test cases which requires a special configuration file (e.g. one field missing).
    
  * To run the test cases, execute the ones which ends with `.sh`, or run `auto_test.sh` in this directory.
  
  * If the test is success, it will produce no outputs. 

# user-authentication-scraper
A web scraper that accesses an array of sites and surveys their methods of user authentication, for a web security course project.

## dependencies, and running the code

### dependencies

At the moment, the only dependency (beyond basic Python packages) is Selenium for web scraping.
Selenium's [official documentation](https://selenium-python.readthedocs.io/getting-started.html#simple-usage) is a very helpful resource for those just getting started.

``` 
pip install selenium        # to install selenium
```

### running the code

Currently, each portion of the project is distinct and must be run on its own from the root directory of the repository. 

Therefore, for instance, if you would like to run a demo of the program that checks if a website has cookie- or token-based authentication methods enabled (by finding all authentication-based cookies and tokens), then you should run the script in `cookies/`. The program output will be located in `cookies/<file_name>.txt`.

Note that the web pages being targeted by the scripts can be changed by manually changing the relevant variables in the code files. This will be modified and polished later, when the project is no longer under heavy development.

## websites used for testing

  *a (non-exhaustive) collection of web pages used throughout the development of this project for testing and benchmarks* 

  - https://www.activision.com/
  - https://www.formula1.com/   *-- cookies only (non-standard HTML structure)*
  - https://www.python.org/
  - https://www.ebay.com/
  - https://soundcloud.com/
  - https://bestbuy.com/    *-- FIDO2*
  - https://twitter.com/i/flow/login *-- home page currently incompatible*
  - https://en.wikipedia.org/
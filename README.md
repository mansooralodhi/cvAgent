
## Anthropic API Keys

Claude Console provides two types of API keys:

1. **Linked (Service User Account) API Key**
   ```text
   sk-ant-api03-xxxxxxxxxxxxxxxx
   ```
2. **Not Linked (Personal) API Key**
   ```text
   sk-ant-usr-xxxxxxxxxxxxxxxx
   ```
You can create and manage API keys from the [Claude Console API Keys page](https://platform.claude.com/settings/keys).


## Store and Load API Keys Using a `.env` File

For local development, we store the API key in a `.env` file instead of hard-coding it in source code, as shown below:
```text
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxx
```
Then, add `.env` to `.gitignore`; this prevent the API key from being exposed in the repository.

Note: Python does not automatically read `.env` files. Therefore, if we write:
```python
import os
api_key = os.environ.get("ANTHROPIC_API_KEY")
```
this will only return a value if `ANTHROPIC_API_KEY` has already been defined in the process environment, which is not generally the case when the variable is stored only in a `.env` file.

This is where `python-dotenv` library comes in:
```python
from dotenv import load_dotenv
load_dotenv()
```
`load_dotenv()` reads `.env` and loads its variables into the environment of current process. After that:
```python
import os
api_key = os.environ.get("ANTHROPIC_API_KEY")
```
can retrieve the value of `ANTHROPIC_API_KEY`.

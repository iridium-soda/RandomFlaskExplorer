# Random test
## Description
This application comes with a built-in functionality that allows you to generate random activity data, simulating real-world usage patterns for testing and demonstration purposes.

Repo is based on https://github.com/iridium-soda/flask-restplus-server-example
## Usage:
1. First steup the target container by simply pulling an image:
    ```shell
    docker run -it --rm --publish 5000:5000 frolvlad/flask-restplus-server-example
    ```
2. Run this script and do data gathering.
    ```shell
    python main.py
    ```

## NOTE
- 由于时间原因暂时不实现多用户切换,所有操作均由admin完成.
- 暂未实现PATCH方法
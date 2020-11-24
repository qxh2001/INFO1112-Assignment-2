import sys
import socket
import os
import gzip


def main():
    pass


if __name__ == '__main__':
    main()


def check_if_string_in_file(file_name, string_to_search):
    # Reference: https://thispointer.com/python-search-strings-in-a-file-and-get-line-numbers-of-lines-containing-the-
    # string/#:~:text=Check%20if%20a%20string%20exists%20in%20a%20file&text=If%20the%20line%20contains%20the,
    # string%2C%20then%20it%20returns%20False.&text=As%20file%20contains%20the%20'is,function%20check_if_string_in_
    # file()%20returns%20True.
    """ Check if any line in the file contains given string """
    global string
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for each_line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in each_line:
                string = each_line
                return True
    return False


# parse the config file, save them inside the list
config = []
if len(sys.argv) < 2:
    print("Missing Configuration Argument")
    sys.exit()
else:
    try:
        f = open(sys.argv[1], "r")
        for lines in f:
            line = lines.strip().split("=")
            config.append(line)
        f.close()
    except FileNotFoundError:
        print("Unable To Load Configuration File")
        sys.exit()

STATIC_FILE = ""
CGI_BIN = ""
PORT = ""
EXEC = ""

content_map = {".txt": "text/plain", ".html": "text/html", ".js": "application/javascript",
               ".css": "text/css", ".jpeg": "image/jpeg", ".xml": "text/xml",
               ".jpg": "image/jpeg", ".png": "image/png"}

# parse the config list, assign each field to variable
i = 0
if len(config) < 4:
    print("Missing Field From Configuration File")
    sys.exit()
else:
    while i < len(config):
        if config[i][0] == 'staticfiles':
            STATIC_FILE = config[i][1]
        elif config[i][0] == 'cgibin':
            CGI_BIN = config[i][1]
        elif config[i][0] == 'port':
            try:
                if not config[i][1].isdigit():
                    raise ValueError("Port Address not Valid")
                else:
                    PORT = int(config[i][1])
            except ValueError as e:
                print("Port Address not Valid")
                sys.exit()
        elif config[i][0] == 'exec':
            EXEC = config[i][1]
        i += 1

# check if any of the field is empty
if STATIC_FILE == "" or CGI_BIN == "" or PORT == "" or EXEC == "":
    print("Missing Field From Configuration File")
    sys.exit()

# initialise some variables and prepare the socket
HOST = 'localhost'
compress = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
os.environ['SERVER_ADDR'] = "127.0.0.1"
os.environ['SERVER_PORT'] = str(PORT)
s.listen()

# connection
while True:
    conn, addr = s.accept()
    # fork to allow multiple connections. This is supposed to work but I don't know why it doesn't!
    pid = os.fork()
    if pid == 0:
        os.environ['REMOTE_ADDRESS'] = addr[0]
        os.environ['REMOTE_PORT'] = str(addr[1])
        data = conn.recv(1024).decode()

        # split the header into various parts and store into the variables
        data_list = data.split("\n")
        data_list_separated = []
        for items in data_list:
            data_list_separated += items.strip().split(": ")
        if "gzip" in data_list_separated:
            compress = True
        os.environ["REQUEST_METHOD"] = data.split(" ")[0]
        filename = data.split(" ")[1]

        # set environment variables
        if "Host" in data_list_separated:
            index = int(data_list_separated.index("Host"))
            os.environ['HTTP_HOST'] = data_list_separated[index + 1]
        if "User-Agent" in data_list_separated:
            index = int(data_list_separated.index("User-Agent"))
            os.environ['HTTP_USER_AGENT'] = data_list_separated[index + 1]
        if "Accept-Encoding" in data_list_separated:
            index = int(data_list_separated.index("Accept-Encoding"))
            os.environ['HTTP_ACCEPT_ENCODING'] = data_list_separated[index + 1]

        # checks for query string
        if "?" in filename:
            filename_list = filename.split("?")
            filename = filename_list[0]
            os.environ['QUERY_STRING'] = filename_list[1]

        if filename == "/":
            filename = "/index.html"
            os.environ["REQUEST_URI"] = filename

        # set filename for connection
        file_extension = os.path.splitext(filename)[1]
        if file_extension == ".sh":
            EXEC = "/bin/bash"
        if filename.split("/")[1] == CGI_BIN.split("/")[1]:  # cgi files
            filename = "." + filename
            os.environ["REQUEST_URI"] = filename.split(".")[1] + file_extension
        else:  # static files
            filename = STATIC_FILE + filename
            os.environ["REQUEST_URI"] = filename

        # map the extension with the content types and save into the environment variables
        if file_extension in content_map:
            content_type = content_map[file_extension]
            os.environ['HTTP_ACCEPT'] = content_type
        else:
            content_type = "text/html"
            os.environ['HTTP_ACCEPT'] = content_type
        if os.environ['REQUEST_METHOD'] == "POST":
            os.environ['CONTENT_TYPE'] = content_type
            os.environ['CONTENT_LENGTH'] = content_type

        try:
            # open the CGI script
            # reference: https://www.tutorialspoint.com/python/os_pipe.htm
            if filename.split("/")[1] == CGI_BIN.split("/")[1]:
                r, w = os.pipe()
                ppid = os.fork()
                if ppid == 0:  # child process
                    # duplicate the file descriptor: stdout and stderr
                    os.dup2(w, 1)  # stdout
                    os.dup2(w, 2)  # stderr
                    try:
                        os.execve(EXEC, [EXEC, filename], os.environ)  # execute the program
                        sys.exit(0)  # exit with code 0 (no exceptions)
                    except:  # case where an exception is caught
                        sys.exit(1)  # exit with code 1 (exception caught)
                elif ppid == -1:  # fork failed due to lack of available resources
                    print("The child process failed to fork.")
                    sys.exit(2)  # exit with code 2 (exception caught, but differentiates from exception in code)
                else:  # parent process
                    status = os.wait()[1]  # get the exit status
                    os.close(w)
                    content = os.fdopen(r, "r").readlines()  # read the content in pipe from child
                    for lines in content:  # check if there's a line containing the content type/ status code/ zip
                        if lines.startswith("Content-Type"):
                            content_type = lines.split(": ")[1]
                        elif lines.startswith("Status-Code"):
                            status_line = lines
                        elif lines.startswith("Accept-Encoding"):
                            if lines.split(": ")[1] == "gzip":
                                compress = True

                # checks the exit status
                if status == 256:  # 500 Internal Server Error
                    header = "HTTP/1.1 500 Internal Server Error\n" + "Content-Type: " + content_type + \
                             "\n" + "Content-Length: " + str(len(content)) + "\n\n"
                    content = "".join(content) + "\n"
                    conn.send(header.encode())
                    conn.send(content.encode())

                elif status == 512:  # 404 File Not Found Error
                    filename = "404.html"
                    with open(filename, 'r') as f:
                        content = f.read()
                    conn.send(("HTTP/1.1 404 File not found\n" + "Content-Type: text/html\n" +
                               "\n").encode())
                    conn.send(content.encode())

                elif status == 0:  # normal execution
                    # check if it needs to be compressed, compress the body of the message and send
                    if compress:
                        header = "HTTP/1.1 200 OK\n" + "Content-Type: " + content_type + "\n" + \
                                 "Accept_Encoding: gzip\n" + "\n\n"
                        content = "".join(content)
                        with open("temp.txt.gz", "w") as f:
                            f.writelines(content)
                        f = open("temp.txt.gz", "rb")
                        the_data = f.read()
                        bindata = bytearray(the_data)
                        f.close()
                        with gzip.open("temp.txt.gz", "wb") as f:
                            f.write(bindata)
                        with open("temp.txt.gz", "rb") as f:
                            data_compressed = f.read()
                        conn.send(header.encode())
                        conn.send(data_compressed)

                    # parse the content type
                    if check_if_string_in_file(filename, "Content-Type"):
                        content_type = string.split('"')[1]
                        header = "HTTP/1.1 200 OK\n" + content_type + "\n\n"
                        content = "".join(content[2:])
                        conn.send(header.encode())
                        conn.send(content.encode())

                    # parse the status code using the function defined at the start
                    elif check_if_string_in_file(filename, "Status-Code"):
                        status_code = status_line.split(" ")[1]
                        status_msg = status_line.split(" ")[2:]
                        status_msg = " ".join(status_msg)
                        header = "HTTP/1.1 " + status_code + " " + status_msg + "\n" + "Content-Type: " + \
                                 content_type + "\n\n"
                        content = "".join(content[2:])
                        conn.send(header.encode())
                        conn.send(content.encode())

                    else:  # no content type and status code declared in the CGI script
                        header = "HTTP/1.1 200 OK\n" + "Content-Type: " + content_type + "\n\n"
                        content = "".join(content)
                        conn.send(header.encode())
                        conn.send(content.encode())

            else:  # all other static files cases
                if content_type == "image/png" or content_type == "image/jpeg":  # image formats
                    with open(filename, 'rb') as f:
                        content = f.read()
                    # check if it needs to be compressed, compress the body of the message and send
                    if compress:
                        header = "HTTP/1.1 200 OK\n" + "Content-Type: " + content_type + "\n" + \
                                 "Accept_Encoding: gzip\n" + "\n\n"
                        with open("temp.txt.gz", "w") as f:
                            f.writelines(content)
                        f = open("temp.txt.gz", "rb")
                        the_data = f.read()
                        bindata = bytearray(the_data)
                        f.close()
                        with gzip.open("temp.txt.gz", "wb") as f:
                            f.write(bindata)
                        with open("temp.txt.gz", "rb") as f:
                            data_compressed = f.read()
                        conn.send(header.encode())
                        conn.send(data_compressed)
                    else:
                        conn.send(("HTTP/1.1 200 OK\n" + "Content-Type: " + content_type
                                   + "\n\n").encode())
                        conn.send(content)
                else:
                    with open(filename, 'r') as f:  # all other format
                        content = f.read()
                    # check if it needs to be compressed, compress the body of the message and send
                    if compress:
                        header = "HTTP/1.1 200 OK\n" + "Content-Type: " + content_type + "\n" + \
                                 "Accept_Encoding: gzip\n" + "\n\n"
                        with open("temp.txt.gz", "w") as f:
                            f.writelines(content)
                        f = open("temp.txt.gz", "rb")
                        the_data = f.read()
                        bindata = bytearray(the_data)
                        f.close()
                        with gzip.open("temp.txt.gz", "wb") as f:
                            f.write(bindata)
                        with open("temp.txt.gz", "rb") as f:
                            data_compressed = f.read()
                        conn.send(header.encode())
                        conn.send(data_compressed)
                    else:
                        conn.send(("HTTP/1.1 200 OK\n" + "Content-Type: " + content_type
                                   + "\n\n").encode())
                        conn.send(content.encode())

        except FileNotFoundError:  # 404 Error page
            filename = "404.html"
            with open(filename, 'r') as f:
                content = f.read()
            conn.send(("HTTP/1.1 404 File not found\n" + "Content-Type: text/html\n" +
                       "Content-Length: " + str(len(content)) + "\n\n").encode())
            conn.send(content.encode())

        sys.exit(0)  # exit the child
    conn.close()  # close the client
s.close()  # although this code is unreachable, it is necessary to close the socket at some point
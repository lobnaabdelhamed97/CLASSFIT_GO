package Helper

import (
  "bytes"
  b64 "encoding/base64"
  "encoding/json"
  "errors"
  "fmt"
  "io"
  "io/ioutil"
  "net/http"
  "os/exec"
  "strings"
)

func python_binds(arg1 string, input map[string]string) (string, error) {
  app := "venv/bin/python3.10"
  arg0 := "kernel/main.py"
  arg2, _ := json.Marshal(input)
  arg2 = []byte(b64.StdEncoding.EncodeToString(arg2))
  arg3 := "2>&1"
  cmd := exec.Command(app, arg0, arg1, string(arg2), arg3)
  var out bytes.Buffer
  var stderr bytes.Buffer
  cmd.Stdout = &out
  cmd.Stderr = &stderr
  err := cmd.Run()
  if err != nil {
    fmt.Println(fmt.Sprint(err) + ": " + stderr.String())
    return "", nil
  }
  if strings.Contains(out.String(), "error") {
    return "", errors.New(out.String())
  } else {
    return out.String(), nil
  }
}

func PaymentCurl(keysec string, url string, input []byte) []byte {

  req, _ := http.NewRequest("POST", url, bytes.NewBuffer(input))

  req.Header.Add("content-type", "application/json")
  req.Header.Add("cache-control", "no-cache")
  req.Header.Add("Key-Sec", keysec)
  res, _ := http.DefaultClient.Do(req)
  defer func(Body io.ReadCloser) {
    err := Body.Close()
    if err != nil {

    }
  }(res.Body)
  body, _ := ioutil.ReadAll(res.Body)
  return body
}
func KeySecured(projectkey string, projectsecret string) string {
  key := projectkey + "-" + projectsecret
  EncodedKey := b64.StdEncoding.EncodeToString([]byte(key))
  return EncodedKey
}

//  func curl(arg1 string, input map[string]string) (string, error){

// payload = "{\n\t\"dict\": {\n\t\t\"key1\": \"value1\",\n\t\t\"key2\": \"value2\"\n\t}\n}"
// headers = {
//     'Content-Type': "application/json",
//     'cache-control': "no-cache",
//     'Postman-Token': <TOKEN>
//     }

// resp, err := requests.Get("https://httpbin.org/", headers, nil)

// postData := &bytes.Buffer{}
// postData.WriteString("postdata")
// resp, err := requests.Post("https://httpbin.org/", headers, &requests.RequestParams{
//     Data:    postData,
// })
// 	if err != nil {
// 		fmt.Println(fmt.Sprint(err) + ": " + stderr.String())
// 		return "", nil
// 	} else {
// 		return resp, nil
// 	}
//  }

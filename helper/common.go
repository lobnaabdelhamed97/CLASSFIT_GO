package common

import (
	"bytes"
	b64 "encoding/base64"
	"encoding/json"
	"errors"
	"fmt"
	"github.com/gin-gonic/gin"
	"os/exec"
	"strings"
)

func python_binds(c *gin.Context, arg1 string, input map[string]string) (string, error) {
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

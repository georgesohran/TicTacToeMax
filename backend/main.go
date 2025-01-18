package backend

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
  r := gin.Default()

  r.GET("/ping", func(ctx *gin.Context) {
    ctx.JSON(http.StatusOK, map[string]any{
      "messege": "PONG",
    })
  })

  r.Run()
}

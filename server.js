const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");
const path = require("path");

const app = express();

app.use(cors());
app.use(express.json());

app.use(
  express.static(
    path.join(__dirname, "public")
  )
);

app.post("/chat", (req, res) => {

  const question = req.body.question;

  exec(
    `python ai_engine.py "${question}"`,
    (error, stdout, stderr) => {

      if (error) {

        console.log(error);

        return res.json({
          result: "AI Error"
        });
      }

      try {

        const result =
          JSON.parse(stdout);

        res.json(result);

      } catch {

        res.json({
          result: "AI วิเคราะห์ไม่สำเร็จ"
        });
      }

    }
  );

});

app.listen(3000, () => {

  console.log("AI Server Running");

});
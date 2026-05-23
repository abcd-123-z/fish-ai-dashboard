const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");
const path = require("path");

const app = express();

app.use(cors());
app.use(express.json());

app.use(express.static(__dirname));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.post("/chat", (req, res) => {

  const question = req.body.question;

  exec(
    `python3 ai_engine.py "${question}"`,
    (error, stdout, stderr) => {

      if (error) {

        console.log(stderr);

        return res.json({
          result: "AI Error"
        });
      }

      try {

        const result = JSON.parse(stdout);

        res.json(result);

      } catch (err) {

        console.log(err);

        res.json({
          result: "AI วิเคราะห์ไม่สำเร็จ"
        });
      }

    }
  );

});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {

  console.log(`Server running on port ${PORT}`);

});
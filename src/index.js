const express = require("express");
const path = require("path");
const router = require("./routes");
const handlebars = require("express-handlebars");
const session = require("express-session");

const port = 3000;
const app = express();

app.use(express.static(path.join(__dirname, "public")));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(
  session({
    secret: "mysecretkey",
    resave: false,
    saveUninitialized: true,
  })
);

app.engine(
  "hbs",
  handlebars.engine({
    extname: ".hbs",
  })
);
app.set("view engine", "hbs");
app.set("views", path.join(__dirname, "/resources/views"));

router(app);

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

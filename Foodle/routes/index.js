const homeRoute = require("./home");
const bodyParser = require("body-parser");

const constructorMethod = app => {

  app.use(bodyParser.json());

  app.use("/", homeRoute);

  //app.use("*", (req, res) => {
    //res.redirect("/");
  //});
};

module.exports = constructorMethod;

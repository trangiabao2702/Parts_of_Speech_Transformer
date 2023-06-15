const siteRoute = require("./site.route");

function router(app) {
  app.use("/", siteRoute);
}

module.exports = router;

const router = require("express").Router();

const siteController = require("../app/controllers/site.controller");

router.get("/tutorial", siteController.tutorial);
router.get("/about_us", siteController.about_us);
router.get("/history", siteController.history);
router.get("/", siteController.home);

router.post("/", siteController.predict);

module.exports = router;

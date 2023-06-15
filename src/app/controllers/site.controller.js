const { PythonShell } = require("python-shell");

function runPythonScript(input_text) {
  return new Promise((resolve, reject) => {
    PythonShell.run("pos.py", { args: [input_text] }, function (err, result) {
      if (err) {
        reject(err);
      } else {
        resolve(result);
      }
    });
  });
}

const siteController = {
  // [GET] /
  home: async (req, res) => {
    // get information in session
    const original_text = req.session.original_text;
    const transformed_text = req.session.transformed_text;

    // clear session
    req.session.original_text = null;
    req.session.transformed_text = null;

    res.render("home", {
      original_text: original_text,
      transformed_text: transformed_text,
    });
  },

  // [POST] /
  predict: async (req, res) => {
    const options = {
      args: [req.body.input_text],
    };

    try {
      await PythonShell.run("pos.py", options).then((message) => {
        req.session.original_text = req.body.input_text;
        req.session.transformed_text = message[0];
      });
    } catch (error) {
      console.log(error);
    }

    res.redirect("/");
  },

  // [GET] /tutorial
  tutorial: async (req, res) => {
    res.render("tutorial");
  },

  // [GET] /about_us
  about_us: async (req, res) => {
    res.render("about_us");
  },

  // [GET] /history
  history: async (req, res) => {
    res.render("history");
  },
};

module.exports = siteController;

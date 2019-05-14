const express = require("express");
const router = express.Router();
const rankingAlgo = require("../data/ranking");

const bodyParser = require('body-parser');

async function getData(userInput) {
    try {
        let generatedList = [];
        generatedList = await rankingAlgo.main(userInput);
        return generatedList;
    } catch (exception) {
        console.log(exception)
    }

}

router.use(bodyParser.json());

let userInput = "";

router.get('/', (req, res) => {

    res.render("frontend");
});

router.post('/abcdefgh', async (req, res) => {
    try {
        let body = req.body;
        if (!body) {
            throw "no Input provided !";
        }
        else
            userInput = body.Ingredient;
        let data = await getData(userInput);
        if (data.length == 0) {
            throw "No recipe Found";
        }
        res.render("result", { data: data });
    }
    catch (error) {
        res.render("result", {
            err: error
        })
    }

});

module.exports = router;
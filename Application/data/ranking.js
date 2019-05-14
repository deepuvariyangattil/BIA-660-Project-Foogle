const mongoCollections = require("../public/mongoCollections");
const recepiedata = mongoCollections.democoll;
const connection = require("../public/mongoConnection");

async function getAll() {
    const recepieCollection = await recepiedata();

    const recepie = await recepieCollection.find({}).toArray();

    return recepie;
}

async function main(input) {
    let userInput=input;

    console.log(userInput)

    const allrecepie = await getAll();
    
    //console.log(userInput);
 
    if (userInput) {
            //console.log("I m here")
            let inputIngredientElement = userInput.split(",")
            let i=0;
            let maxMatchCount = 0;
            inputIngredientElement.forEach(Ingredient => {
              Ingredient = Ingredient.trim();
              inputIngredientElement[i]=Ingredient;
              //console.log(inputIngredientElement[i])
              i++;
            });

            allrecepie.forEach(thisrecepie => {
                thisrecepie.matchCount = 0;
                thisrecepie.matchedList = [];
                thisrecepie.pagerank = 0;
                let Ingredientlist = (thisrecepie.Recipe).toString().split(",");
                //console.log(Ingredientlist)
                thisrecepie.totalIngredient = Object.keys(Ingredientlist).length;
                //console.log("Total Ingredients: "+ thisrecepie.totalIngredient);
                
                //Ingredientlist.forEach(thisIngredientList => {
                 inputIngredientElement.forEach(thisinputIngredientElement => {  
                    let flag =0;
                    Ingredientlist.forEach(thisIngredientList => {
                        if(thisIngredientList.includes(thisinputIngredientElement) && flag==0){
                            thisrecepie.matchedList.push(thisinputIngredientElement);
							//console.log("Ingredient: " + thisinputIngredientElement)
                            //console.log("matched: " + thisinputIngredientElement + " with: " + thisIngredientList)
                            thisrecepie.matchCount++;
                            flag++;
                        }   
                    })
                })
                //console.log("Total Matches: "+ thisrecepie.matchCount);
                thisrecepie.pagerank = parseFloat(thisrecepie.matchCount / thisrecepie.totalIngredient);
                if(thisrecepie.matchCount > maxMatchCount){
                    maxMatchCount = thisrecepie.matchCount;
                }
                //console.log("PageRank: "+ thisrecepie.pagerank);
                //console.log("------------------------------------------");
                
            })

            console.log("maxMatchCount: ",maxMatchCount);
            //console.log(allrecepie);
			
			let SelectedRecepie = [];
            
            let flag =0;
			allrecepie.forEach(thisrecepie => {	
				if((thisrecepie.pagerank != 0) && flag < 25 ){
                    SelectedRecepie.push(thisrecepie)
                    flag++;
                }
                /*if(thisrecepie.matchCount == maxMatchCount){
                    console.log(thisrecepie.Titles);
                    SelectedRecepie.push(thisrecepie)
                }*/
			})
			
            SelectedRecepie.sort((a, b) => (a.pagerank < b.pagerank) ? 1 : -1);
            SelectedRecepie.sort((a,b) => (a.matchCount < b.matchCount)? 1 : -1);
			return SelectedRecepie; 
    }   

const db = await connection();
//await db.serverConfig.close();
console.log("Done!");
}

computeRank();

function computeRank(){
    main().catch(error => {
        console.log(error);
      });
}

module.exports = {
    firstName: "Neeshit", 
    lastName: "Dangi", 
    studentId: "10439010",
    main
};
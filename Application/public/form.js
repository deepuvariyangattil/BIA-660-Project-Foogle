const mongoCollections = require("./mongoCollections");
/*const recepiedata = mongoCollections.recepiedata;
const connection = require("./mongoConnection");*/

(function () {

    const mongoCollections = require("./mongoCollections");
    
    const primechecker = document.getElementById("Ingredientchecker");

    if (primechecker) {

        primechecker.addEventListener("submit", event => {
            event.preventDefault();
            const primeNumberElement = document.getElementById("Ingredient");
            let primeNumber = primeNumberElement.value;
          
            if(!primeNumber){
                let error = document.getElementById("error");
                error.className = "error-Container-display";
                error.innerHTML="Enter Number";
            }
            else{
                let error = document.getElementById("error");
                error.className = "error-Container-hide";
                error.innerHTML="";
                let li = document.createElement("li");
                li.className = "is-primeNumber";
                let node = document.createTextNode(primeNumber);
                li.appendChild(node);
                let ol = document.getElementById("attempts");
                ol.appendChild(li);
                
                
            }
               
            
            
        });
    }
})();

function isPrimeNumber(n)
{

  if (n===1)
  {
    return false;
  }
  else if(n === 2)
  {
    return true;
  }else
  {
    for(var x = 2; x < n; x++)
    {
      if(n % x === 0)
      {
        return false;
      }
    }
    return true;  
  }
}
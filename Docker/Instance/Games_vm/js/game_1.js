const options = {
  aroma: "Aroma agradable",
  pimienta: "Companera de la sal",
  detener: "Poner fin a algo",
  saltar: "Subir de manera repentina",
  barajar: "Mezclar las cartas",
  combinar: "Anadir; Mezclar",
  caos: "Desorden total",
  laberinto: "Maze",
  perturbar: "Interrumpir; molestar",
  cambiar: "Mover; Periodo de trabajo",
  maquina: "Dispositivo o aparato",
  espejo: "Superficie lisa y reflectante",
  estrella: "Objeto luminoso en el cielo",
  jardin: "Area al aire libre con plantas",
  amarillo: "Color entre verde y naranja",
  libro: "Conjunto de hojas escritas",
  buho: "Ave nocturna",
  guitarra: "Instrumento musical de cuerda",
  taza: "Recipiente para beber",
  ala: "Extremidad del ave",
  carretera: "Via para vehiculos",
  sol: "Estrella que ilumina la Tierra",
  sombrero: "Cubierta para la cabeza",
  dulce: "Golosina o postre",
  cielo: "Espacio que rodea la Tierra",
  mar: "Gran masa de agua salada",
  cima: "Parte mas alta de una montana",
  amor: "Sentimiento afectuoso",
  almohada: "Cojin para dormir",
  castillo: "Edificio fortificado",
  elefante: "Animal grande con trompa",
  luna: "Satelite natural de la Tierra",
  musica: "Sonidos organizados en el tiempo",
  arbol: "Planta con tronco y ramas",
  agua: "Liquido incoloro e inodoro",
  bote: "Pequena embarcacion",
  casa: "Vivienda para personas",
  perro: "Animal de compania",
  tierra: "Planeta habitado por seres vivos",
  aguila: "Ave rapaz",
  ojo: "Organo de la vision",
  flor: "Estructura reproductiva de las plantas",
  zapato: "Calzado para proteger los pies",
  dragon: "Criatura mitica con alas y escamas"
};

//Initial References
const message = document.getElementById("message");
const hintRef = document.querySelector(".hint-ref");
const controls = document.querySelector(".controls-container");
const startBtn = document.getElementById("start");
const letterContainer = document.getElementById("letter-container");
const userInpSection = document.getElementById("user-input-section");
const resultText = document.getElementById("result");
const word = document.getElementById("word");
const words = Object.keys(options);
let randomWord = "",
  randomHint = "";
let winCount = 0,
  lossCount = 0;

//Generate random value
const generateRandomValue = (array) => Math.floor(Math.random() * array.length);

//Block all the buttons
const blocker = () => {
  let lettersButtons = document.querySelectorAll(".letters");
  stopGame();
};

//Start Game
startBtn.addEventListener("click", () => {
  controls.classList.add("hide");
  init();
});

//Stop Game
const stopGame = () => {
  controls.classList.remove("hide");
};

//Generate Word Function
const generateWord = () => {
  letterContainer.classList.remove("hide");
  userInpSection.innerText = "";
  randomWord = words[generateRandomValue(words)];
  randomHint = options[randomWord];
  hintRef.innerHTML = `<div id="wordHint">
  <span>Hint: </span>${randomHint}</div>`;
  let displayItem = "";
  randomWord.split("").forEach((value) => {
    displayItem += '<span class="inputSpace">_ </span>';
  });

  //Display each element as span
  userInpSection.innerHTML = displayItem;
  userInpSection.innerHTML += `<div id='chanceCount'>Chances Left: ${lossCount}</div>`;
};

//Initial Function
const init = () => {
  winCount = 0;
  lossCount = 5;
  randomWord = "";
  word.innerText = "";
  randomHint = "";
  message.innerText = "";
  userInpSection.innerHTML = "";
  letterContainer.classList.add("hide");
  letterContainer.innerHTML = "";
  generateWord();

  //For creating letter buttons
  for (let i = 65; i < 91; i++) {
    let button = document.createElement("button");
    button.classList.add("letters");

    //Number to ASCII[A-Z]
    button.innerText = String.fromCharCode(i);

    //Character button onclick
    button.addEventListener("click", () => {
      message.innerText = `Correct Letter`;
      message.style.color = "#008000";
      let charArray = randomWord.toUpperCase().split("");
      let inputSpace = document.getElementsByClassName("inputSpace");

      //If array contains clicked value replace the matched Dash with Letter
      if (charArray.includes(button.innerText)) {
        charArray.forEach((char, index) => {
          //If character in array is same as clicked button
          if (char === button.innerText) {
            button.classList.add("correct");
            //Replace dash with letter
            inputSpace[index].innerText = char;
            //increment counter
            winCount += 1;
            //If winCount equals word length
            if (winCount == charArray.length) {
              resultText.innerHTML = "You Won";
              startBtn.innerText = "Restart";
              //block all buttons
              blocker();
            }
          }
        });
      } else {
        //lose count
        button.classList.add("incorrect");
        lossCount -= 1;
        document.getElementById(
          "chanceCount"
        ).innerText = `Chances Left: ${lossCount}`;
        message.innerText = `Incorrect Letter`;
        message.style.color = "#ff0000";
        if (lossCount == 0) {
          word.innerHTML = `The word was: <span>${randomWord}</span>`;
          resultText.innerHTML = "Game Over";
          blocker();
        }
      }

      //Disable clicked buttons
      button.disabled = true;
    });

    //Append generated buttons to the letters container
    letterContainer.appendChild(button);
  }
};

window.onload = () => {
  init();
};
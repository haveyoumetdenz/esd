// app.js

const firebase = require("firebase/app");
require("firebase/auth");
require("firebase/firestore");

const firebaseConfig1 = require("./firebase1");
const firebaseConfig2 = require("./firebase2");

const app1 = firebase.initializeApp(firebaseConfig1, "app1");
const app2 = firebase.initializeApp(firebaseConfig2, "app2");

// Use app1 and app2 for different Firebase instances
const auth1 = app1.auth();
const firestore1 = app1.firestore();

const auth2 = app2.auth();
const firestore2 = app2.firestore();

// Other code in your application

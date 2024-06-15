let layers = [];
let weights = [];
let errors = [];
let learningRate = 0.1;

function setup() {
    let canvas = createCanvas(800, 600);
    canvas.parent('ml-animation');

    // Create layers
    layers = [
        [{ x: 100, y: 150 }, { x: 100, y: 250 }, { x: 100, y: 350 }],  // Input layer
        [{ x: 300, y: 100 }, { x: 300, y: 200 }, { x: 300, y: 300 }, { x: 300, y: 400 }],  // Hidden layer
        [{ x: 500, y: 150 }, { x: 500, y: 250 }, { x: 500, y: 350 }]   // Output layer
    ];

    // Initialize weights randomly
    weights = [
        Array.from({ length: layers[0].length }, () => Array.from({ length: layers[1].length }, () => random(-1, 1))),
        Array.from({ length: layers[1].length }, () => Array.from({ length: layers[2].length }, () => random(-1, 1)))
    ];

    // Initialize errors to zero
    errors = Array(layers[2].length).fill(0);
}

function draw() {
    background(255);

    // Draw neurons
    for (let i = 0; i < layers.length; i++) {
        for (let j = 0; j < layers[i].length; j++) {
            fill(200);
            stroke(0);
            ellipse(layers[i][j].x, layers[i][j].y, 40, 40);
        }
    }

    // Draw weights
    stroke(0);
    for (let i = 0; i < weights.length; i++) {
        for (let j = 0; j < weights[i].length; j++) {
            for (let k = 0; k < weights[i][j].length; k++) {
                let start = layers[i][j];
                let end = layers[i + 1][k];
                strokeWeight(map(abs(weights[i][j][k]), 0, 1, 1, 5));
                line(start.x, start.y, end.x, end.y);
            }
        }
    }

    // Simulate forward pass and backpropagation
    if (frameCount % 60 === 0) {
        console.log("Performing forward pass and backpropagation");

        // Forward pass
        let inputs = [1, 0, 1]; // Example inputs
        let hiddenOutputs = layers[1].map((_, j) => activationFunction(dotProduct(inputs, weights[0].map(w => w[j]))));
        let outputs = layers[2].map((_, k) => activationFunction(dotProduct(hiddenOutputs, weights[1].map(w => w[k]))));

        console.log("Inputs:", inputs);
        console.log("Hidden Outputs:", hiddenOutputs);
        console.log("Outputs:", outputs);

        // Calculate errors
        let target = [0, 1, 0]; // Example target
        errors = outputs.map((output, k) => output - target[k]);

        console.log("Errors:", errors);

        // Backpropagation
        // Update weights for output layer
        for (let k = 0; k < weights[1].length; k++) {
            for (let j = 0; j < weights[1][k].length; j++) {
                weights[1][k][j] -= learningRate * errors[j] * hiddenOutputs[k];
            }
        }

        // Update weights for hidden layer
        for (let j = 0; j < weights[0].length; j++) {
            for (let i = 0; i < weights[0][j].length; i++) {
                let hiddenError = errors.reduce((sum, err, k) => sum + err * weights[1][k][j], 0);
                weights[0][j][i] -= learningRate * hiddenError * inputs[i];
            }
        }

        console.log("Updated Weights:", weights);
    }

    // Display errors
    fill(0);
    noStroke();
    textSize(16);
    text(`Errors: ${errors.map(e => e.toFixed(2)).join(', ')}`, 10, height - 10);
}

function dotProduct(vec1, vec2) {
    return vec1.reduce((sum, v, i) => sum + v * vec2[i], 0);
}

function activationFunction(x) {
    return 1 / (1 + exp(-x)); // Sigmoid function
}

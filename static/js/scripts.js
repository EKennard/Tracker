let weightUnit = 'kg';
let heightUnit = 'cm';

        //  Harris-Benedict Equation
        //  (https://www.omnicalculator.com/health/bmr-harris-benedict-equation)
        // For men: BMR = 66.5 + (13.75 × weight in kg) + (5.003 × height in cm) - (6.75 × age)
        //  For women: BMR = 655.1 + (9.563 × weight in kg) + (1.850 × height in cm) - (4.676 × age)
        //  Sedentary (little or no exercise): calories = BMR × 1.2;
        //  Lightly active (light exercise/sports 1-3 days/week): calories = BMR × 1.375;
        //  Moderately active (moderate exercise/sports 3-5 days/week): calories = BMR × 1.55;
        //  Very active (hard exercise/sports 6-7 days a week): calories = BMR × 1.725
        //  Extra active (very hard exercise/sports & a physical job): calories = BMR × 1.9; and
        //  Professional athlete: calories = BMR × 2.3

function lbToKg(lb) {
    return lb / 2.20462;
}

function ftInToCm(feet, inches) {
    return (feet * 30.48) + (inches * 2.54);
}

function calculateCalorieNeeds({ 
    weight, weightUnit, 
    height, heightUnit, 
    sex, age 
}) {
    // convert weight to kg
    let weight_kg = (weightUnit === 'lb') ? lbToKg(weight) : weight;

    // converts height to cm
    let height_cm;
    if (heightUnit === 'cm') {
        height_cm = height;
    } else if (heightUnit === 'ft') {
        // height should be an object: {feet: x, inches: y}
        height_cm = ftInToCm(height.feet, height.inches);
    } else {
        height_cm = height;
    }

    // calculate BMR
    let bmr;
    if (sex.toLowerCase() === 'female') {
        bmr = 655.1 + (9.563 * weight_kg) + (1.850 * height_cm) - (4.676 * age);
    } else {
        bmr = 66.5 + (13.75 * weight_kg) + (5.003 * height_cm) - (6.75 * age);
    }
    return bmr;
}

const bmr = calculateCalorieNeeds(userData);
console.log('BMR:', bmr);
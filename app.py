from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

workout_plans = {
    "Weight Loss": "Full Body workout, 4 days a week\nDay 1: Chest and Back\nDay 2: Arms and Shoulder\nDay 3: Legs\nDay 4: Cardio",
    "Fat Loss": "Intensive Cardio workout, 5 days a week\nDay 1: HIIT Training\nDay 2: Running\nDay 3: Cycling\nDay 4: Jump Rope\nDay 5: Swimming",
    "Weight Gain": "Split workout, 5 days a week\nDay 1: Chest\nDay 2: Back\nDay 3: Legs\nDay 4: Shoulders\nDay 5: Arms",
    "Muscle Gain": "Strength Training, 3 days a week\nDay 1: Upper Body\nDay 2: Lower Body\nDay 3: Full Body",
    "Overall Fitness": "Mixed workout plan, 6 days a week\nDay 1: Cardio\nDay 2: Strength Training\nDay 3: Yoga\nDay 4: Pilates\nDay 5: HIIT\nDay 6: Rest"
}

meal_plans = {
    "Weight Loss": "<p>Day 1:<br><br>Breakfast: Scrambled eggs with spinach and whole grain toast<br>Lunch: Grilled chicken salad with mixed greens, tomatoes, cucumbers, and balsamic vinaigrette<br>Dinner: Baked chicken breast with brown rice and steamed broccoli<br><br>Day 2:<br><br>Breakfast: Whole grain toast with avocado and poached eggs<br>Lunch: Pasta salad with grilled chicken, cherry tomatoes, and pesto dressing<br>Dinner: Whole wheat spaghetti with tomato sauce and baked fish fillet<br><br>Day 3:<br><br>Breakfast: Greek yogurt with berries and honey<br>Lunch: Grilled fish tacos with coleslaw and avocado<br>Dinner: Stir-fried vegetables with tofu over brown rice<br><br>Day 4:<br><br>Breakfast: Oatmeal with sliced bananas and almonds<br>Lunch: Quinoa salad with roasted vegetables and feta cheese<br>Dinner: Vegetable stir-fry with tofu and whole wheat noodles<br><br>Day 5:<br><br>Breakfast: Smoothie with spinach, banana, almond milk, and protein powder<br>Lunch: Greek salad with mixed greens, olives, feta cheese, and grilled chicken<br>Dinner: Grilled salmon with roasted sweet potatoes and asparagus<br><br>Day 6:<br><br>Breakfast: Whole grain toast with peanut butter and sliced strawberries<br>Lunch: Lentil soup with whole grain bread<br>Dinner: Baked potato with diced ham, broccoli, and cheese<br><br>Day 7:<br><br>Breakfast: Veggie omelette with mushrooms, bell peppers, and onions<br>Lunch: Quinoa bowl with black beans, corn, avocado, and salsa<br>Dinner: Grilled steak with roasted Brussels sprouts and mashed potatoes</p>",
    "Fat Loss": "<p>Day 1:<br><br>Breakfast: Protein shake with banana and almond milk<br>Lunch: Grilled chicken breast with steamed broccoli<br>Dinner: Baked salmon with quinoa and asparagus<br><br>Day 2:<br><br>Breakfast: Greek yogurt with berries<br>Lunch: Turkey wrap with lettuce and tomato<br>Dinner: Stir-fried vegetables with tofu over brown rice<br><br>Day 3:<br><br>Breakfast: Oatmeal with sliced strawberries<br>Lunch: Mixed greens salad with grilled shrimp<br>Dinner: Baked chicken with roasted sweet potatoes<br><br>Day 4:<br><br>Breakfast: Scrambled eggs with spinach<br>Lunch: Tuna salad with mixed greens<br>Dinner: Grilled steak with roasted Brussels sprouts<br><br>Day 5:<br><br>Breakfast: Avocado toast with poached eggs<br>Lunch: Quinoa salad with black beans and corn<br>Dinner: Grilled turkey burgers with lettuce wraps<br><br>Day 6:<br><br>Breakfast: Protein pancakes with mixed berries<br>Lunch: Grilled chicken Caesar salad<br>Dinner: Baked cod with steamed vegetables<br><br>Day 7:<br><br>Breakfast: Smoothie with kale, pineapple, and protein powder<br>Lunch: Veggie stir-fry with tofu<br>Dinner: Grilled shrimp with quinoa and broccoli</p>",
    "Weight Gain": "<p>Day 1:<br><br>Breakfast: Omelette with cheese, spinach, and mushrooms<br>Lunch: Turkey sandwich with avocado and whole grain bread<br>Dinner: Baked chicken thighs with sweet potato mash and green beans<br><br>Day 2:<br><br>Breakfast: Protein pancakes with sliced bananas<br>Lunch: Beef stir-fry with mixed vegetables and rice<br>Dinner: Grilled salmon with quinoa salad<br><br>Day 3:<br><br>Breakfast: Greek yogurt with granola and berries<br>Lunch: Chicken Caesar salad with croutons<br>Dinner: Spaghetti with meatballs and garlic bread<br><br>Day 4:<br><br>Breakfast: Breakfast burrito with eggs, cheese, and salsa<br>Lunch: Tuna salad sandwich with whole wheat bread<br>Dinner: BBQ ribs with mashed potatoes and coleslaw<br><br>Day 5:<br><br>Breakfast: Smoothie with protein powder, peanut butter, and banana<br>Lunch: Grilled chicken wrap with lettuce and tomato<br>Dinner: Beef chili with cornbread<br><br>Day 6:<br><br>Breakfast: Bagel with cream cheese and smoked salmon<br>Lunch: Turkey burger with avocado and sweet potato fries<br>Dinner: Pork chops with roasted vegetables<br><br>Day 7:<br><br>Breakfast: Breakfast sandwich with egg, cheese, and bacon<br>Lunch: Veggie pizza with whole wheat crust<br>Dinner: Chicken Alfredo pasta with garlic bread</p>",
    "Muscle Gain": "<p>Day 1:<br><br>Breakfast: Protein oats with berries<br>Lunch: Chicken breast with quinoa and mixed vegetables<br>Dinner: Steak with sweet potato and broccoli<br><br>Day 2:<br><br>Breakfast: Greek yogurt with granola and honey<br>Lunch: Tuna salad with whole wheat crackers<br>Dinner: Grilled salmon with brown rice and asparagus<br><br>Day 3:<br><br>Breakfast: Scrambled eggs with spinach and whole wheat toast<br>Lunch: Turkey wrap with avocado and lettuce<br>Dinner: Beef stir-fry with rice noodles and vegetables<br><br>Day 4:<br><br>Breakfast: Protein smoothie with banana and almond milk<br>Lunch: Grilled chicken salad with nuts and dried fruits<br>Dinner: Pork chops with roasted potatoes and green beans<br><br>Day 5:<br><br>Breakfast: Cottage cheese with pineapple and almonds<br>Lunch: Quinoa salad with grilled shrimp and avocado<br>Dinner: Chicken breast with pasta and marinara sauce<br><br>Day 6:<br><br>Breakfast: Protein pancakes with mixed berries<br>Lunch: Beef burrito bowl with black beans and salsa<br>Dinner: Grilled turkey breast with couscous and vegetables<br><br>Day 7:<br><br>Breakfast: Omelette with cheese, mushrooms, and peppers<br>Lunch: Chicken and vegetable stir-fry with brown rice<br>Dinner: Steak with mashed potatoes and steamed carrots</p>",
    "Overall Fitness": "<p>Day 1:<br><br>Breakfast: Smoothie with spinach, banana, almond milk, and protein powder<br>Lunch: Grilled chicken salad with mixed greens, tomatoes, cucumbers, and balsamic vinaigrette<br>Dinner: Baked salmon with quinoa and asparagus<br><br>Day 2:<br><br>Breakfast: Greek yogurt with granola and berries<br>Lunch: Turkey wrap with avocado and lettuce<br>Dinner: Beef stir-fry with rice noodles and vegetables<br><br>Day 3:<br><br>Breakfast: Oatmeal with sliced strawberries<br>Lunch: Mixed greens salad with grilled shrimp<br>Dinner: Grilled chicken breast with steamed broccoli and brown rice<br><br>Day 4:<br><br>Breakfast: Scrambled eggs with spinach and whole wheat toast<br>Lunch: Tuna salad sandwich with whole wheat bread<br>Dinner: Grilled steak with sweet potato mash and green beans<br><br>Day 5:<br><br>Breakfast: Avocado toast with poached eggs<br>Lunch: Quinoa salad with black beans, corn, and avocado<br>Dinner: Baked cod with roasted vegetables<br><br>Day 6:<br><br>Breakfast: Protein pancakes with mixed berries<br>Lunch: Chicken Caesar salad with croutons<br>Dinner: Vegetable stir-fry with tofu over brown rice<br><br>Day 7:<br><br>Breakfast: Veggie omelette with mushrooms, bell peppers, and onions<br>Lunch: Lentil soup with whole grain bread<br>Dinner: Grilled shrimp with quinoa and broccoli</p>"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendation')
def recommendation():
    return render_template('recommendation.html')


@app.route('/recommended', methods=['POST'])
def recommended():
    data = request.get_json()
    selected_goal_label = data['goal']

    workout = workout_plans.get(selected_goal_label)
    meal_plan = meal_plans.get(selected_goal_label)

    return jsonify({
        'workout': workout,
        'meal_plan': meal_plan
    })

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/tracking')
def tracking():
    return render_template('tracking.html')

if __name__ == '__main__':
    app.run(debug=True)


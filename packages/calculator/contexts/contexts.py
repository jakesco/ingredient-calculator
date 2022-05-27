def main(args):
    return {
        "units": units,
        "contexts": contexts,
    }


units = ("oz", "gram", "floz", "cup", "tsp", "tbsp")

contexts = (
    "Water (contexts)",
    "All-Purpose Flour",
    "Almond Flour",
    "Almond meal",
    "Almond paste (packed)",
    "Almonds (sliced)",
    "Almonds (slivered)",
    "Almonds, whole (unblanched)",
    "Amaranth flour",
    "Apple juice concentrate",
    "Apples (dried, diced)",
    "Apples (peeled, sliced)",
    "Applesauce",
    "Apricots (dried, diced)",
    "Artisan Bread Flour",
    "Artisan Bread Topping",
    "Baker's Cinnamon Filling",
    "Baker's Fruit Blend",
    "Baker's Special Sugar (superfine sugar, castor sugar)",
    "Baking powder",
    "Baking soda",
    "Baking Sugar Alternative",
    "Bananas (mashed)",
    "Barley (cooked)",
    "Barley (pearled)",
    "Barley flakes",
    "Barley flour",
    "Barley malt syrup",
    "Basil pesto",
    "Bell peppers (fresh)",
    "Berries (frozen)",
    "Blueberries (dried)",
    "Blueberries (fresh)",
    "Blueberry juice",
    "Boiled cider",
    "Bran cereal",
    "Bread crumbs (dried)",
    "Bread crumbs (fresh)",
    "Bread crumbs (Japanese Panko)",
    "Bread Flour",
    "Brown rice (cooked)",
    "Brown rice flour",
    "Brown sugar (dark or light, packed)",
    "Buckwheat (whole)",
    "Buckwheat Flour",
    "Bulgur",
    "Butter",
    "Buttermilk",
    "Buttermilk powder",
    "Cacao nibs",
    "Cake Enhancer",
    "Candied peel",
    "Caramel (14-16 individual pieces, 1in squares)",
    "Caramel bits (chopped Heath or toffee)",
    "Caraway seeds",
    "Carrots (cooked and puréed)",
    "Carrots (diced)",
    "Carrots (grated)",
    "Cashews (chopped)",
    "Cashews (whole)",
    "Celery (diced)",
    "Cheese (Feta)",
    "Cheese (grated cheddar, jack, mozzarella, or Swiss)",
    "Cheese (grated Parmesan)",
    "Cheese (Ricotta)",
    "Cherries (candied)",
    "Cherries (dried)",
    "Cherries (fresh, pitted, chopped)",
    "Cherries (frozen)",
    "Cherry Concentrate",
    "Chickpea flour",
    "Chives (fresh)",
    "Chocolate (chopped)",
    "Chocolate Chips",
    "Chocolate Chunks",
    "Cinnamon Sweet Bits",
    "Cinnamon-Sugar",
    "Cocoa (unsweetened)",
    "Coconut (sweetened, shredded)",
    "Coconut (toasted)",
    "Coconut (unsweetened, desiccated)",
    "Coconut (unsweetened, large flakes)",
    "Coconut (unsweetened, shredded)",
    "Coconut Flour",
    "Coconut Milk Powder",
    "Coconut oil",
    "Coconut sugar",
    "Confectioners' sugar (unsifted)",
    "Cookie crumbs",
    "Corn (popped)",
    "Corn syrup",
    "Cornmeal (whole)",
    "Cornmeal (yellow, Quaker)",
    "Cornstarch",
    "Cracked wheat",
    "Cranberries (dried)",
    "Cranberries (fresh or frozen)",
    "Cream (heavy cream, light cream, or half & half)",
    "Cream cheese",
    "Crystallized ginger",
    "Currants",
    "Dates (chopped)",
    "Demerara sugar",
    "Dried Blueberry Powder",
    "Dried milk (Baker's Special Dry Milk)",
    "Dried nonfat milk (powdered)",
    "Dried potato flakes (instant mashed potatoes)",
    "Dried whole milk (powdered)",
    "Durum Flour",
    "Easy Roll Dough Improver",
    "Egg (fresh)",
    "Egg white (fresh)",
    "Egg whites (dried)",
    "Egg yolk (fresh)",
    "Espresso Powder",
    "Everything Bagel Topping",
    "Figs (dried, chopped)",
    "First Clear Flour",
    "Flax meal",
    "Flaxseed",
    "French-Style Flour",
    "Fruitcake Fruit Blend",
    "Garlic (cloves, in skin for roasting)",
    "Garlic (minced)",
    "Garlic (peeled and sliced)",
    "Ginger (fresh, sliced)",
    "Gluten-Free All-Purpose Baking Mix",
    "Gluten-Free All-Purpose Flour",
    "Gluten-Free Measure for Measure Flour",
    "Graham cracker crumbs (boxed)",
    "Graham crackers (crushed)",
    "Granola",
    "Grape Nuts",
    "Harvest Grains Blend",
    "Hazelnut flour",
    "Hazelnut Praline Paste",
    "Hazelnut spread",
    "Hazelnuts (whole)",
    "Hi-Maize Natural Fiber",
    "High-Gluten Flour",
    "Honey",
    "Instant ClearJel",
    "Irish-Style Flour",
    "Italian-Style Flour",
    "Jam or preserves",
    "Jammy Bits",
    "Keto Wheat Flour",
    "Key Lime Juice",
    "Lard",
    "Leeks (diced)",
    "Lemon Juice Powder",
    "Lime Juice Powder",
    "Macadamia nuts (whole)",
    "Malt syrup",
    "Malted Milk Powder",
    "Malted Wheat Flakes",
    "Maple sugar",
    "Maple syrup",
    "Marshmallow crème",
    "Marshmallow Fluff®",
    "Marshmallows (mini)",
    "Marzipan",
    "Mascarpone cheese",
    "Mashed potatoes",
    "Mayonnaise",
    "Medium Rye Flour",
    "Meringue powder",
    "Milk (evaporated)",
    "Milk (fresh)",
    "Millet (whole)",
    "Mini chocolate chips",
    "Molasses",
    "Mushrooms (sliced)",
    "Non-Diastatic Malt Powder",
    "Oat bran",
    "Oat flour",
    "Oats (old-fashioned or quick-cooking)",
    "Olive oil",
    "Olives (sliced)",
    "Onions (fresh, diced)",
    "Paleo Baking Flour",
    "Palm shortening",
    "Passion fruit purée ",
    "Pasta Flour Blend",
    "Pastry Flour",
    "Pastry Flour Blend",
    "Peaches (peeled and diced)",
    "Peanut butter",
    "Peanuts (whole, shelled)",
    "Pears (peeled and diced)",
    "Pecan Meal",
    "Pecans (diced)",
    "Pie Filling Enhancer",
    "Pine nuts",
    "Pineapple (dried)",
    "Pineapple (fresh or canned, diced)",
    "Pistachio nuts (shelled)",
    "Pistachio Paste",
    "Pizza Dough Flavor",
    "Pizza Flour",
    "Pizza Flour Blend",
    "Polenta (coarse ground cornmeal)",
    "Poppy seeds",
    "Potato Flour",
    "Potato starch",
    "Pumpernickel Flour",
    "Pumpkin purée ",
    "Quinoa (cooked)",
    "Quinoa (whole)",
    "Quinoa flour",
    "Raisins (loose)",
    "Raisins (packed)",
    "Raspberries (fresh)",
    "Rhubarb (sliced, 1/2in slices)",
    "Rice (long grain, dry)",
    "Rice flour (white)",
    "Rice Krispies",
    "Rye Bread Improver",
    "Rye Chops",
    "Rye flakes",
    "Rye Flour Blend",
    "Salt (Kosher, Diamond Crystal)",
    "Salt (Kosher, Morton's)",
    "Salt (table)",
    "Scallions (sliced)",
    "Self-Rising Flour",
    "Semolina Flour",
    "Sesame seeds",
    "Shallots (peeled and sliced)",
    "Six-Grain Blend",
    "Sorghum flour",
    "Sour cream",
    "Sourdough starter",
    "Soy flour",
    "Sparkling Sugar",
    "Spelt Flour",
    "Sprouted Wheat Flour",
    "Steel cut oats",
    "Sticky Bun Sugar",
    "Strawberries (fresh sliced)",
    "Sugar (granulated white)",
    "Sugar substitute (Splenda)",
    "Sundried tomatoes (dry pack)",
    "Sunflower seeds",
    "Super 10 Blend",
    "Sweet Ground Chocolate and Cocoa Blend",
    "Sweetened condensed milk",
    "Tahini paste",
    "Tapioca starch or flour",
    "Tapioca (quick cooking)",
    "Teff flour",
    "The Works Bread Topping",
    "Toasted Almond Flour",
    "Toffee chunks",
    "Tropical Fruit Blend",
    "Turbinado sugar (raw)",
    "Unbleached Cake Flour",
    "Vanilla Extract ",
    "Vegetable oil",
    "Vegetable shortening",
    "Vermont Cheese Powder",
    "Vital Wheat Gluten",
    "Walnuts (chopped)",
    "Walnuts (whole)",
    "Wheat berries (red)",
    "Wheat bran",
    "Wheat germ",
    "White Chocolate Chips",
    "White Rye Flour",
    "White Whole Wheat Flour",
    "Whole Grain Flour Blend",
    "Whole Wheat Flour (Premium 100%)",
    "Whole Wheat Pastry Flour / Graham Flour",
    "Yeast (instant)",
    "Yogurt",
    "Zucchini (shredded)",
)
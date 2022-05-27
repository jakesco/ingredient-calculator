from dataclasses import dataclass
from fractions import Fraction

from pint import Context, UnitRegistry


def main(args):
    # Parse request
    if not (request := Request.from_json(args)):
        return {"conversion": "-"}

    # Initialize unit registry
    ureg = UnitRegistry()
    c = Context(request.context.name)
    c.add_transformation("[volume]", "[mass]", request.context.make_vol_to_mass())
    c.add_transformation("[mass]", "[volume]", request.context.make_mass_to_vol())
    ureg.add_context(c)
    Q_ = ureg.Quantity

    conversion = request.multiplier * Q_(request.amount, request.from_unit).to(request.to_unit, request.context.name)

    return {"conversion": f"{float(conversion.magnitude):.3f} {conversion.units}(s)"}


@dataclass(frozen=True)
class ContextBuilder:
    name: str
    amount: float
    unit: str
    ounces: float

    def make_vol_to_mass(self):
        return lambda u, x: (x * self.ounces * u.oz) / (
            self.amount * u.parse_units(self.unit)
        )

    def make_mass_to_vol(self):
        return lambda u, x: (x * self.amount * u.parse_units(self.unit)) / (
            self.ounces * u.oz
        )


@dataclass(frozen=True)
class Request:
    context: ContextBuilder
    amount: Fraction
    from_unit: str
    to_unit: str
    multiplier: Fraction

    @classmethod
    def from_json(cls, args):
        return cls(
            context=CONTEXTS[args.get('context')],
            amount=Fraction(args.get('amount')),
            from_unit=args.get('from_unit'),
            to_unit=args.get('to_unit'),
            multiplier=args.get('multiplier'),
        )


UNITS = ("oz", "gram", "floz", "cup", "tsp", "tbsp")

CONTEXTS = {
    "Water (contexts)": ContextBuilder("Water (contexts)", 1, "cup", 8),
    "All-Purpose Flour": ContextBuilder("All-Purpose Flour", 1.0, "cup", 4.25),
    "Almond Flour": ContextBuilder("Almond Flour", 1.0, "cup", 3.375),
    "Almond meal": ContextBuilder("Almond meal", 1.0, "cup", 3.0),
    "Almond paste (packed)": ContextBuilder("Almond paste (packed)", 1.0, "cup", 9.125),
    "Almonds (sliced)": ContextBuilder("Almonds (sliced)", 0.5, "cup", 1.5),
    "Almonds (slivered)": ContextBuilder("Almonds (slivered)", 0.5, "cup", 2.0),
    "Almonds, whole (unblanched)": ContextBuilder(
        "Almonds, whole (unblanched)", 1.0, "cup", 5.0
    ),
    "Amaranth flour": ContextBuilder("Amaranth flour", 1.0, "cup", 3.625),
    "Apple juice concentrate": ContextBuilder(
        "Apple juice concentrate", 0.25, "cup", 2.5
    ),
    "Apples (dried, diced)": ContextBuilder("Apples (dried, diced)", 1.0, "cup", 3.0),
    "Apples (peeled, sliced)": ContextBuilder(
        "Apples (peeled, sliced)", 1.0, "cup", 4.0
    ),
    "Applesauce": ContextBuilder("Applesauce", 1.0, "cup", 9.0),
    "Apricots (dried, diced)": ContextBuilder(
        "Apricots (dried, diced)", 0.5, "cup", 2.25
    ),
    "Artisan Bread Flour": ContextBuilder("Artisan Bread Flour", 1.0, "cup", 4.25),
    "Artisan Bread Topping": ContextBuilder("Artisan Bread Topping", 0.25, "cup", 1.5),
    "Baker's Cinnamon Filling": ContextBuilder(
        "Baker's Cinnamon Filling", 1.0, "cup", 5.375
    ),
    "Baker's Fruit Blend": ContextBuilder("Baker's Fruit Blend", 1.0, "cup", 4.5),
    "Baker's Special Sugar (superfine sugar, castor sugar)": ContextBuilder(
        "Baker's Special Sugar (superfine sugar, castor sugar)", 1.0, "cup", 6.75
    ),
    "Baking powder": ContextBuilder("Baking powder", 1.0, "teaspoon", 0.1410958),
    "Baking soda": ContextBuilder("Baking soda", 0.5, "teaspoon", 0.1058219),
    "Baking Sugar Alternative": ContextBuilder(
        "Baking Sugar Alternative", 1.0, "cup", 6.0
    ),
    "Bananas (mashed)": ContextBuilder("Bananas (mashed)", 1.0, "cup", 8.0),
    "Barley (cooked)": ContextBuilder("Barley (cooked)", 1.0, "cup", 7.625),
    "Barley (pearled)": ContextBuilder("Barley (pearled)", 1.0, "cup", 7.5),
    "Barley flakes": ContextBuilder("Barley flakes", 0.5, "cup", 1.625),
    "Barley flour": ContextBuilder("Barley flour", 1.0, "cup", 3.0),
    "Barley malt syrup": ContextBuilder("Barley malt syrup", 2.0, "tablespoons", 1.5),
    "Basil pesto": ContextBuilder("Basil pesto", 2.0, "tablespoons", 1.0),
    "Bell peppers (fresh)": ContextBuilder("Bell peppers (fresh)", 1.0, "cup", 5.0),
    "Berries (frozen)": ContextBuilder("Berries (frozen)", 1.0, "cup", 5.0),
    "Blueberries (dried)": ContextBuilder("Blueberries (dried)", 1.0, "cup", 5.5),
    "Blueberries (fresh)": ContextBuilder("Blueberries (fresh)", 1.0, "cup", 6.0),
    "Blueberry juice": ContextBuilder("Blueberry juice", 1.0, "cup", 8.5),
    "Boiled cider": ContextBuilder("Boiled cider", 0.25, "cup", 3.0),
    "Bran cereal": ContextBuilder("Bran cereal", 1.0, "cup", 2.125),
    "Bread crumbs (dried)": ContextBuilder("Bread crumbs (dried)", 0.25, "cup", 1.0),
    "Bread crumbs (fresh)": ContextBuilder("Bread crumbs (fresh)", 0.25, "cup", 0.75),
    "Bread crumbs (Japanese Panko)": ContextBuilder(
        "Bread crumbs (Japanese Panko)", 1.0, "cup", 1.75
    ),
    "Bread Flour": ContextBuilder("Bread Flour", 1.0, "cup", 4.25),
    "Brown rice (cooked)": ContextBuilder("Brown rice (cooked)", 1.0, "cup", 6.0),
    "Brown rice flour": ContextBuilder("Brown rice flour", 1.0, "cup", 4.5),
    "Brown sugar (dark or light, packed)": ContextBuilder(
        "Brown sugar (dark or light, packed)", 1.0, "cup", 7.5
    ),
    "Buckwheat (whole)": ContextBuilder("Buckwheat (whole)", 1.0, "cup", 6.0),
    "Buckwheat Flour": ContextBuilder("Buckwheat Flour", 1.0, "cup", 4.25),
    "Bulgur": ContextBuilder("Bulgur", 1.0, "cup", 5.375),
    "Butter": ContextBuilder("Butter", 8.0, "tablespoons", 4.0),
    "Buttermilk": ContextBuilder("Buttermilk", 1.0, "cup", 8.0),
    "Buttermilk powder": ContextBuilder(
        "Buttermilk powder", 2.0, "tablespoons", 0.6666666666666666
    ),
    "Cacao nibs": ContextBuilder("Cacao nibs", 1.0, "cup", 4.25),
    "Cake Enhancer": ContextBuilder("Cake Enhancer", 2.0, "tablespoons", 0.5),
    "Candied peel": ContextBuilder("Candied peel", 0.5, "cup", 3.0),
    "Caramel (14-16 individual pieces, 1in squares)": ContextBuilder(
        "Caramel (14-16 individual pieces, 1in squares)", 0.5, "cup", 5.0
    ),
    "Caramel bits (chopped Heath or toffee)": ContextBuilder(
        "Caramel bits (chopped Heath or toffee)", 1.0, "cup", 5.5
    ),
    "Caraway seeds": ContextBuilder("Caraway seeds", 2.0, "tablespoons", 0.625),
    "Carrots (cooked and puréed)": ContextBuilder(
        "Carrots (cooked and puréed)", 0.5, "cup", 4.5
    ),
    "Carrots (diced)": ContextBuilder("Carrots (diced)", 1.0, "cup", 5.0),
    "Carrots (grated)": ContextBuilder("Carrots (grated)", 1.0, "cup", 3.5),
    "Cashews (chopped)": ContextBuilder("Cashews (chopped)", 1.0, "cup", 4.0),
    "Cashews (whole)": ContextBuilder("Cashews (whole)", 1.0, "cup", 4.0),
    "Celery (diced)": ContextBuilder("Celery (diced)", 1.0, "cup", 5.0),
    "Cheese (Feta)": ContextBuilder("Cheese (Feta)", 0.5, "cup", 2.0),
    "Cheese (grated cheddar, jack, mozzarella, or Swiss)": ContextBuilder(
        "Cheese (grated cheddar, jack, mozzarella, or Swiss)", 1.0, "cup", 4.0
    ),
    "Cheese (grated Parmesan)": ContextBuilder(
        "Cheese (grated Parmesan)", 0.5, "cup", 1.75
    ),
    "Cheese (Ricotta)": ContextBuilder("Cheese (Ricotta)", 1.0, "cup", 8.0),
    "Cherries (candied)": ContextBuilder("Cherries (candied)", 0.25, "cup", 1.75),
    "Cherries (dried)": ContextBuilder("Cherries (dried)", 0.5, "cup", 2.5),
    "Cherries (fresh, pitted, chopped)": ContextBuilder(
        "Cherries (fresh, pitted, chopped)", 0.5, "cup", 2.875
    ),
    "Cherries (frozen)": ContextBuilder("Cherries (frozen)", 1.0, "cup", 4.0),
    "Cherry Concentrate": ContextBuilder("Cherry Concentrate", 2.0, "tablespoons", 1.5),
    "Chickpea flour": ContextBuilder("Chickpea flour", 1.0, "cup", 3.0),
    "Chives (fresh)": ContextBuilder("Chives (fresh)", 0.5, "cup", 0.75),
    "Chocolate (chopped)": ContextBuilder("Chocolate (chopped)", 1.0, "cup", 6.0),
    "Chocolate Chips": ContextBuilder("Chocolate Chips", 1.0, "cup", 6.0),
    "Chocolate Chunks": ContextBuilder("Chocolate Chunks", 1.0, "cup", 6.0),
    "Cinnamon Sweet Bits": ContextBuilder("Cinnamon Sweet Bits", 1.0, "cup", 5.0),
    "Cinnamon-Sugar": ContextBuilder("Cinnamon-Sugar", 0.25, "cup", 1.75),
    "Cocoa (unsweetened)": ContextBuilder("Cocoa (unsweetened)", 0.5, "cup", 1.5),
    "Coconut (sweetened, shredded)": ContextBuilder(
        "Coconut (sweetened, shredded)", 1.0, "cup", 3.0
    ),
    "Coconut (toasted)": ContextBuilder("Coconut (toasted)", 1.0, "cup", 3.0),
    "Coconut (unsweetened, desiccated)": ContextBuilder(
        "Coconut (unsweetened, desiccated)", 1.0, "cup", 3.0
    ),
    "Coconut (unsweetened, large flakes)": ContextBuilder(
        "Coconut (unsweetened, large flakes)", 1.0, "cup", 2.125
    ),
    "Coconut (unsweetened, shredded)": ContextBuilder(
        "Coconut (unsweetened, shredded)", 1.0, "cup", 1.875
    ),
    "Coconut Flour": ContextBuilder("Coconut Flour", 1.0, "cup", 4.5),
    "Coconut Milk Powder": ContextBuilder("Coconut Milk Powder", 0.5, "cup", 2.0),
    "Coconut oil": ContextBuilder("Coconut oil", 0.5, "cup", 4.0),
    "Coconut sugar": ContextBuilder("Coconut sugar", 0.5, "cup", 2.75),
    "Confectioners' sugar (unsifted)": ContextBuilder(
        "Confectioners' sugar (unsifted)", 2.0, "cups", 8.0
    ),
    "Cookie crumbs": ContextBuilder("Cookie crumbs", 1.0, "cup", 3.0),
    "Corn (popped)": ContextBuilder("Corn (popped)", 4.0, "cups", 0.75),
    "Corn syrup": ContextBuilder("Corn syrup", 1.0, "cup", 11.0),
    "Cornmeal (whole)": ContextBuilder("Cornmeal (whole)", 1.0, "cup", 4.875),
    "Cornmeal (yellow, Quaker)": ContextBuilder(
        "Cornmeal (yellow, Quaker)", 1.0, "cup", 5.5
    ),
    "Cornstarch": ContextBuilder("Cornstarch", 0.25, "cup", 1.0),
    "Cracked wheat": ContextBuilder("Cracked wheat", 1.0, "cup", 5.25),
    "Cranberries (dried)": ContextBuilder("Cranberries (dried)", 0.5, "cup", 2.0),
    "Cranberries (fresh or frozen)": ContextBuilder(
        "Cranberries (fresh or frozen)", 1.0, "cup", 3.5
    ),
    "Cream (heavy cream, light cream, or half & half)": ContextBuilder(
        "Cream (heavy cream, light cream, or half & half)", 1.0, "cup", 8.0
    ),
    "Cream cheese": ContextBuilder("Cream cheese", 1.0, "cup", 8.0),
    "Crystallized ginger": ContextBuilder("Crystallized ginger", 0.5, "cup", 3.25),
    "Currants": ContextBuilder("Currants", 1.0, "cup", 5.0),
    "Dates (chopped)": ContextBuilder("Dates (chopped)", 1.0, "cup", 5.25),
    "Demerara sugar": ContextBuilder("Demerara sugar", 1.0, "cup", 7.75),
    "Dried Blueberry Powder": ContextBuilder(
        "Dried Blueberry Powder", 0.25, "cup", 1.0
    ),
    "Dried milk (Baker's Special Dry Milk)": ContextBuilder(
        "Dried milk (Baker's Special Dry Milk)", 0.25, "cup", 1.0
    ),
    "Dried nonfat milk (powdered)": ContextBuilder(
        "Dried nonfat milk (powdered)", 0.25, "cup", 1.0
    ),
    "Dried potato flakes (instant mashed potatoes)": ContextBuilder(
        "Dried potato flakes (instant mashed potatoes)", 0.5, "cup", 1.5
    ),
    "Dried whole milk (powdered)": ContextBuilder(
        "Dried whole milk (powdered)", 0.5, "cup", 1.75
    ),
    "Durum Flour": ContextBuilder("Durum Flour", 1.0, "cup", 4.375),
    "Easy Roll Dough Improver": ContextBuilder(
        "Easy Roll Dough Improver", 2.0, "tablespoons", 0.625
    ),
    "Egg (fresh)": ContextBuilder("Egg (fresh)", 1.0, "large", 1.75),
    "Egg white (fresh)": ContextBuilder("Egg white (fresh)", 1.0, "large", 1.25),
    "Egg whites (dried)": ContextBuilder(
        "Egg whites (dried)", 2.0, "tablespoons", 0.375
    ),
    "Egg yolk (fresh)": ContextBuilder("Egg yolk (fresh)", 1.0, "large", 0.5),
    "Espresso Powder": ContextBuilder("Espresso Powder", 1.0, "tablespoon", 0.25),
    "Everything Bagel Topping": ContextBuilder(
        "Everything Bagel Topping", 0.25, "cup", 1.25
    ),
    "Figs (dried, chopped)": ContextBuilder("Figs (dried, chopped)", 1.0, "cup", 5.25),
    "First Clear Flour": ContextBuilder("First Clear Flour", 1.0, "cup", 3.75),
    "Flax meal": ContextBuilder("Flax meal", 0.5, "cup", 1.75),
    "Flaxseed": ContextBuilder("Flaxseed", 0.25, "cup", 1.25),
    "French-Style Flour": ContextBuilder("French-Style Flour", 1.0, "cup", 4.25),
    "Fruitcake Fruit Blend": ContextBuilder("Fruitcake Fruit Blend", 1.0, "cup", 4.25),
    "Garlic (cloves, in skin for roasting)": ContextBuilder(
        "Garlic (cloves, in skin for roasting)", 1.0, "large", 4.0
    ),
    "Garlic (minced)": ContextBuilder("Garlic (minced)", 2.0, "tablespoons", 1.0),
    "Garlic (peeled and sliced)": ContextBuilder(
        "Garlic (peeled and sliced)", 1.0, "cup", 5.25
    ),
    "Ginger (fresh, sliced)": ContextBuilder(
        "Ginger (fresh, sliced)", 0.25, "cup", 2.0
    ),
    "Gluten-Free All-Purpose Baking Mix": ContextBuilder(
        "Gluten-Free All-Purpose Baking Mix", 1.0, "cup", 4.25
    ),
    "Gluten-Free All-Purpose Flour": ContextBuilder(
        "Gluten-Free All-Purpose Flour", 1.0, "cup", 5.5
    ),
    "Gluten-Free Measure for Measure Flour": ContextBuilder(
        "Gluten-Free Measure for Measure Flour", 1.0, "cup", 4.25
    ),
    "Graham cracker crumbs (boxed)": ContextBuilder(
        "Graham cracker crumbs (boxed)", 1.0, "cup", 3.5
    ),
    "Graham crackers (crushed)": ContextBuilder(
        "Graham crackers (crushed)", 1.0, "cup", 5.0
    ),
    "Granola": ContextBuilder("Granola", 1.0, "cup", 4.0),
    "Grape Nuts": ContextBuilder("Grape Nuts", 0.5, "cup", 2.0),
    "Harvest Grains Blend": ContextBuilder("Harvest Grains Blend", 0.5, "cup", 2.625),
    "Hazelnut flour": ContextBuilder("Hazelnut flour", 1.0, "cup", 3.125),
    "Hazelnut Praline Paste": ContextBuilder("Hazelnut Praline Paste", 0.5, "cup", 5.5),
    "Hazelnut spread": ContextBuilder("Hazelnut spread", 0.5, "cup", 5.625),
    "Hazelnuts (whole)": ContextBuilder("Hazelnuts (whole)", 1.0, "cup", 5.0),
    "Hi-Maize Natural Fiber": ContextBuilder(
        "Hi-Maize Natural Fiber", 0.25, "cup", 1.125
    ),
    "High-Gluten Flour": ContextBuilder("High-Gluten Flour", 1.0, "cup", 4.25),
    "Honey": ContextBuilder("Honey", 1.0, "tablespoon", 0.75),
    "Instant ClearJel": ContextBuilder("Instant ClearJel", 1.0, "tablespoon", 0.375),
    "Irish-Style Flour": ContextBuilder("Irish-Style Flour", 1.0, "cup", 3.875),
    "Italian-Style Flour": ContextBuilder("Italian-Style Flour", 1.0, "cup", 3.75),
    "Jam or preserves": ContextBuilder("Jam or preserves", 0.25, "cup", 3.0),
    "Jammy Bits": ContextBuilder("Jammy Bits", 1.0, "cup", 6.5),
    "Keto Wheat Flour": ContextBuilder("Keto Wheat Flour", 1.0, "cup", 4.25),
    "Key Lime Juice": ContextBuilder("Key Lime Juice", 1.0, "cup", 8.0),
    "Lard": ContextBuilder("Lard", 0.5, "cup", 4.0),
    "Leeks (diced)": ContextBuilder("Leeks (diced)", 1.0, "cup", 3.25),
    "Lemon Juice Powder": ContextBuilder(
        "Lemon Juice Powder", 2.0, "tablespoons", 0.625
    ),
    "Lime Juice Powder": ContextBuilder("Lime Juice Powder", 2.0, "tablespoons", 0.625),
    "Macadamia nuts (whole)": ContextBuilder(
        "Macadamia nuts (whole)", 1.0, "cup", 5.25
    ),
    "Malt syrup": ContextBuilder("Malt syrup", 2.0, "tablespoons", 1.5),
    "Malted Milk Powder": ContextBuilder("Malted Milk Powder", 0.25, "cup", 1.25),
    "Malted Wheat Flakes": ContextBuilder("Malted Wheat Flakes", 0.5, "cup", 2.25),
    "Maple sugar": ContextBuilder("Maple sugar", 0.5, "cup", 2.75),
    "Maple syrup": ContextBuilder("Maple syrup", 0.5, "cup", 5.5),
    "Marshmallow crème": ContextBuilder("Marshmallow crème", 1.0, "cup", 3.0),
    "Marshmallow Fluff®": ContextBuilder("Marshmallow Fluff®", 1.0, "cup", 4.5),
    "Marshmallows (mini)": ContextBuilder("Marshmallows (mini)", 1.0, "cup", 1.5),
    "Marzipan": ContextBuilder("Marzipan", 1.0, "cup", 10.125),
    "Mascarpone cheese": ContextBuilder("Mascarpone cheese", 1.0, "cup", 8.0),
    "Mashed potatoes": ContextBuilder("Mashed potatoes", 1.0, "cup", 7.5),
    "Mayonnaise": ContextBuilder("Mayonnaise", 0.5, "cup", 4.0),
    "Medium Rye Flour": ContextBuilder("Medium Rye Flour", 1.0, "cup", 3.75),
    "Meringue powder": ContextBuilder("Meringue powder", 0.25, "cup", 1.5),
    "Milk (evaporated)": ContextBuilder("Milk (evaporated)", 0.5, "cup", 4.0),
    "Milk (fresh)": ContextBuilder("Milk (fresh)", 1.0, "cup", 8.0),
    "Millet (whole)": ContextBuilder("Millet (whole)", 0.5, "cup", 3.625),
    "Mini chocolate chips": ContextBuilder("Mini chocolate chips", 1.0, "cup", 6.25),
    "Molasses": ContextBuilder("Molasses", 0.25, "cup", 3.0),
    "Mushrooms (sliced)": ContextBuilder("Mushrooms (sliced)", 1.0, "cup", 2.75),
    "Non-Diastatic Malt Powder": ContextBuilder(
        "Non-Diastatic Malt Powder", 2.0, "tablespoons", 0.625
    ),
    "Oat bran": ContextBuilder("Oat bran", 0.5, "cup", 1.875),
    "Oat flour": ContextBuilder("Oat flour", 1.0, "cup", 3.25),
    "Oats (old-fashioned or quick-cooking)": ContextBuilder(
        "Oats (old-fashioned or quick-cooking)", 1.0, "cup", 3.125
    ),
    "Olive oil": ContextBuilder("Olive oil", 0.25, "cup", 1.75),
    "Olives (sliced)": ContextBuilder("Olives (sliced)", 1.0, "cup", 5.0),
    "Onions (fresh, diced)": ContextBuilder("Onions (fresh, diced)", 1.0, "cup", 5.0),
    "Paleo Baking Flour": ContextBuilder("Paleo Baking Flour", 1.0, "cup", 3.625),
    "Palm shortening": ContextBuilder("Palm shortening", 0.25, "cup", 1.5),
    "Passion fruit purée ": ContextBuilder(
        "Passion fruit purée ", 0.3333333333333333, "cup", 2.125
    ),
    "Pasta Flour Blend": ContextBuilder("Pasta Flour Blend", 1.0, "cup", 5.125),
    "Pastry Flour": ContextBuilder("Pastry Flour", 1.0, "cup", 3.75),
    "Pastry Flour Blend": ContextBuilder("Pastry Flour Blend", 1.0, "cup", 4.0),
    "Peaches (peeled and diced)": ContextBuilder(
        "Peaches (peeled and diced)", 1.0, "cup", 6.0
    ),
    "Peanut butter": ContextBuilder("Peanut butter", 0.5, "cup", 4.75),
    "Peanuts (whole, shelled)": ContextBuilder(
        "Peanuts (whole, shelled)", 1.0, "cup", 5.0
    ),
    "Pears (peeled and diced)": ContextBuilder(
        "Pears (peeled and diced)", 1.0, "cup", 5.75
    ),
    "Pecan Meal": ContextBuilder("Pecan Meal", 1.0, "cup", 2.75),
    "Pecans (diced)": ContextBuilder("Pecans (diced)", 0.5, "cup", 2.0),
    "Pie Filling Enhancer": ContextBuilder("Pie Filling Enhancer", 0.25, "cup", 1.625),
    "Pine nuts": ContextBuilder("Pine nuts", 0.5, "cup", 2.5),
    "Pineapple (dried)": ContextBuilder("Pineapple (dried)", 0.5, "cup", 2.5),
    "Pineapple (fresh or canned, diced)": ContextBuilder(
        "Pineapple (fresh or canned, diced)", 1.0, "cup", 6.0
    ),
    "Pistachio nuts (shelled)": ContextBuilder(
        "Pistachio nuts (shelled)", 0.5, "cup", 2.125
    ),
    "Pistachio Paste": ContextBuilder("Pistachio Paste", 0.25, "cup", 2.75),
    "Pizza Dough Flavor": ContextBuilder(
        "Pizza Dough Flavor", 2.0, "tablespoons", 0.4232875
    ),
    "Pizza Flour": ContextBuilder("Pizza Flour", 1.0, "cup", 4.0),
    "Pizza Flour Blend": ContextBuilder("Pizza Flour Blend", 1.0, "cup", 4.375),
    "Polenta (coarse ground cornmeal)": ContextBuilder(
        "Polenta (coarse ground cornmeal)", 1.0, "cup", 5.75
    ),
    "Poppy seeds": ContextBuilder("Poppy seeds", 2.0, "tablespoons", 0.625),
    "Potato Flour": ContextBuilder("Potato Flour", 0.25, "cup", 1.625),
    "Potato starch": ContextBuilder("Potato starch", 1.0, "cup", 5.375),
    "Pumpernickel Flour": ContextBuilder("Pumpernickel Flour", 1.0, "cup", 3.75),
    "Pumpkin purée ": ContextBuilder("Pumpkin purée ", 1.0, "cup", 8.0),
    "Quinoa (cooked)": ContextBuilder("Quinoa (cooked)", 1.0, "cup", 6.5),
    "Quinoa (whole)": ContextBuilder("Quinoa (whole)", 1.0, "cup", 6.25),
    "Quinoa flour": ContextBuilder("Quinoa flour", 1.0, "cup", 3.875),
    "Raisins (loose)": ContextBuilder("Raisins (loose)", 1.0, "cup", 5.25),
    "Raisins (packed)": ContextBuilder("Raisins (packed)", 0.5, "cup", 3.0),
    "Raspberries (fresh)": ContextBuilder("Raspberries (fresh)", 1.0, "cup", 4.25),
    "Rhubarb (sliced, 1/2in slices)": ContextBuilder(
        "Rhubarb (sliced, 1/2in slices)", 1.0, "cup", 4.25
    ),
    "Rice (long grain, dry)": ContextBuilder("Rice (long grain, dry)", 0.5, "cup", 3.5),
    "Rice flour (white)": ContextBuilder("Rice flour (white)", 1.0, "cup", 5.0),
    "Rice Krispies": ContextBuilder("Rice Krispies", 1.0, "cup", 1.0),
    "Rye Bread Improver": ContextBuilder(
        "Rye Bread Improver", 2.0, "tablespoons", 0.4938355
    ),
    "Rye Chops": ContextBuilder("Rye Chops", 1.0, "cup", 4.25),
    "Rye flakes": ContextBuilder("Rye flakes", 1.0, "cup", 4.375),
    "Rye Flour Blend": ContextBuilder("Rye Flour Blend", 1.0, "cup", 3.75),
    "Salt (Kosher, Diamond Crystal)": ContextBuilder(
        "Salt (Kosher, Diamond Crystal)", 1.0, "tablespoon", 0.2821917
    ),
    "Salt (Kosher, Morton's)": ContextBuilder(
        "Salt (Kosher, Morton's)", 1.0, "tablespoon", 0.5643834
    ),
    "Salt (table)": ContextBuilder("Salt (table)", 1.0, "tablespoon", 0.6349313),
    "Scallions (sliced)": ContextBuilder("Scallions (sliced)", 1.0, "cup", 2.25),
    "Self-Rising Flour": ContextBuilder("Self-Rising Flour", 1.0, "cup", 4.0),
    "Semolina Flour": ContextBuilder("Semolina Flour", 1.0, "cup", 5.75),
    "Sesame seeds": ContextBuilder("Sesame seeds", 0.5, "cup", 2.5),
    "Shallots (peeled and sliced)": ContextBuilder(
        "Shallots (peeled and sliced)", 1.0, "cup", 5.5
    ),
    "Six-Grain Blend": ContextBuilder("Six-Grain Blend", 1.0, "cup", 4.5),
    "Sorghum flour": ContextBuilder("Sorghum flour", 1.0, "cup", 4.875),
    "Sour cream": ContextBuilder("Sour cream", 1.0, "cup", 8.0),
    "Sourdough starter": ContextBuilder("Sourdough starter", 1.0, "cup", 8.25),
    "Soy flour": ContextBuilder("Soy flour", 0.25, "cup", 1.25),
    "Sparkling Sugar": ContextBuilder("Sparkling Sugar", 0.25, "cup", 2.0),
    "Spelt Flour": ContextBuilder("Spelt Flour", 1.0, "cup", 3.5),
    "Sprouted Wheat Flour": ContextBuilder("Sprouted Wheat Flour", 1.0, "cup", 4.0),
    "Steel cut oats": ContextBuilder("Steel cut oats", 0.5, "cup", 2.5),
    "Sticky Bun Sugar": ContextBuilder("Sticky Bun Sugar", 1.0, "cup", 3.5),
    "Strawberries (fresh sliced)": ContextBuilder(
        "Strawberries (fresh sliced)", 1.0, "cup", 5.875
    ),
    "Sugar (granulated white)": ContextBuilder(
        "Sugar (granulated white)", 1.0, "cup", 7.0
    ),
    "Sugar substitute (Splenda)": ContextBuilder(
        "Sugar substitute (Splenda)", 1.0, "cup", 0.875
    ),
    "Sundried tomatoes (dry pack)": ContextBuilder(
        "Sundried tomatoes (dry pack)", 1.0, "cup", 6.0
    ),
    "Sunflower seeds": ContextBuilder("Sunflower seeds", 0.25, "cup", 1.25),
    "Super 10 Blend": ContextBuilder("Super 10 Blend", 1.0, "cup", 3.75),
    "Sweet Ground Chocolate and Cocoa Blend": ContextBuilder(
        "Sweet Ground Chocolate and Cocoa Blend", 0.25, "cup", 1.0
    ),
    "Sweetened condensed milk": ContextBuilder(
        "Sweetened condensed milk", 0.25, "cup", 2.75
    ),
    "Tahini paste": ContextBuilder("Tahini paste", 0.5, "cup", 4.5),
    "Tapioca starch or flour": ContextBuilder(
        "Tapioca starch or flour", 1.0, "cup", 4.0
    ),
    "Tapioca (quick cooking)": ContextBuilder(
        "Tapioca (quick cooking)", 2.0, "tablespoons", 0.75
    ),
    "Teff flour": ContextBuilder("Teff flour", 1.0, "cup", 4.75),
    "The Works Bread Topping": ContextBuilder(
        "The Works Bread Topping", 0.25, "cup", 1.25
    ),
    "Toasted Almond Flour": ContextBuilder("Toasted Almond Flour", 1.0, "cup", 3.375),
    "Toffee chunks": ContextBuilder("Toffee chunks", 1.0, "cup", 5.5),
    "Tropical Fruit Blend": ContextBuilder("Tropical Fruit Blend", 1.0, "cup", 4.75),
    "Turbinado sugar (raw)": ContextBuilder("Turbinado sugar (raw)", 1.0, "cup", 6.375),
    "Unbleached Cake Flour": ContextBuilder("Unbleached Cake Flour", 1.0, "cup", 4.25),
    "Vanilla Extract ": ContextBuilder("Vanilla Extract ", 1.0, "tablespoon", 0.5),
    "Vegetable oil": ContextBuilder("Vegetable oil", 1.0, "cup", 7.0),
    "Vegetable shortening": ContextBuilder("Vegetable shortening", 0.25, "cup", 1.625),
    "Vermont Cheese Powder": ContextBuilder("Vermont:  Cheese Powder", 0.5, "cup", 2.0),
    "Vital Wheat Gluten": ContextBuilder(
        "Vita: l Wheat Gluten", 2.0, "tablespoons", 0.625
    ),
    "Walnuts (chopped)": ContextBuilder("Wal: nuts (chopped)", 1.0, "cup", 4.0),
    "Walnuts (whole)": ContextBuilder("W: alnuts (whole)", 0.5, "cup", 2.25),
    "Wheat berries (red)": ContextBuilder("Wheat:  berries (red)", 1.0, "cup", 6.5),
    "Wheat bran": ContextBuilder("Wheat bran", 0.5, "cup", 1.125),
    "Wheat germ": ContextBuilder("Wheat germ", 0.25, "cup", 1.0),
    "White Chocolate Chips": ContextBuilder("White C: hocolate Chips", 1.0, "cup", 6.0),
    "White Rye Flour": ContextBuilder("W: hite Rye Flour", 1.0, "cup", 3.75),
    "White Whole Wheat Flour": ContextBuilder(
        "White Who: le Wheat Flour", 1.0, "cup", 4.0
    ),
    "Whole Grain Flour Blend": ContextBuilder(
        "Whole Gra: in Flour Blend", 1.0, "cup", 4.0
    ),
    "Whole Wheat Flour (Premium 100%)": ContextBuilder(
        "Whole Wheat Flour (Premium 100%)", 1.0, "cup", 4.0
    ),
    "Whole Wheat Pastry Flour / Graham Flour": ContextBuilder(
        "Whole Wheat Pastry Flour / Graham Flour", 1.0, "cup", 3.375
    ),
    "Yeast (instant)": ContextBuilder(
        "Yeast (instant)", 1.0, "tablespoon", 0.3333333333333333
    ),
    "Yogurt": ContextBuilder("Yogurt", 1.0, "cup", 8.0),
    "Zucchini (shredded)": ContextBuilder("Zucchini (shredded)", 1.0, "cup", 4.75),
}

if __name__ == "__main__":
    x = main({})
    print(x)
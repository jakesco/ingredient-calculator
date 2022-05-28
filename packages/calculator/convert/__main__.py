from dataclasses import dataclass
from fractions import Fraction
from typing import Callable

from pint import Context, UnitRegistry


def main(args):
    # Parse request
    if not (request := Request.from_json(args)):
        return {"body": "-"}

    # Initialize unit registry
    ureg = UnitRegistry()
    c = Context(request.name)
    c.add_transformation("[volume]", "[mass]", request.context.make_vol_to_mass())
    c.add_transformation("[mass]", "[volume]", request.context.make_mass_to_vol())
    ureg.add_context(c)
    Q_ = ureg.Quantity

    conversion = request.multiplier * Q_(request.amount, request.from_unit).to(
        request.to_unit, request.name
    )

    return {"body": f"{float(conversion.magnitude):.3f} {conversion.units}(s)"}


@dataclass(frozen=True)
class ConversionContext:
    volume: float
    unit: str
    ounces: float

    def make_vol_to_mass(self) -> Callable[[float, float], float]:
        return lambda u, x: (x * self.ounces * u.oz) / (
            self.volume * u.parse_units(self.unit)
        )

    def make_mass_to_vol(self) -> Callable[[float, float], float]:
        return lambda u, x: (x * self.volume * u.parse_units(self.unit)) / (
            self.ounces * u.oz
        )


@dataclass(frozen=True)
class Request:
    name: str
    context: ConversionContext
    amount: Fraction
    from_unit: str
    to_unit: str
    multiplier: Fraction

    @classmethod
    def from_json(cls, args):
        try:
            ctx: str = args.get("context")
            ctx = ctx.replace("+", " ")
            return cls(
                name=args.get("context"),
                context=CONTEXTS[ctx],
                amount=Fraction(args.get("amount")),
                from_unit=args.get("from_unit"),
                to_unit=args.get("to_unit"),
                multiplier=Fraction(args.get("multiplier")),
            )
        except:
            return None


UNITS = ("oz", "gram", "floz", "cup", "tsp", "tbsp")

CONTEXTS = {
    "Water (default)": ConversionContext(1, "cup", 8),
    "All-Purpose Flour": ConversionContext(1.0, "cup", 4.25),
    "Almond Flour": ConversionContext(1.0, "cup", 3.375),
    "Almond meal": ConversionContext(1.0, "cup", 3.0),
    "Almond paste (packed)": ConversionContext(1.0, "cup", 9.125),
    "Almonds (sliced)": ConversionContext(0.5, "cup", 1.5),
    "Almonds (slivered)": ConversionContext(0.5, "cup", 2.0),
    "Almonds, whole (unblanched)": ConversionContext(1.0, "cup", 5.0),
    "Amaranth flour": ConversionContext(1.0, "cup", 3.625),
    "Apple juice concentrate": ConversionContext(0.25, "cup", 2.5),
    "Apples (dried, diced)": ConversionContext(1.0, "cup", 3.0),
    "Apples (peeled, sliced)": ConversionContext(1.0, "cup", 4.0),
    "Applesauce": ConversionContext(1.0, "cup", 9.0),
    "Apricots (dried, diced)": ConversionContext(0.5, "cup", 2.25),
    "Artisan Bread Flour": ConversionContext(1.0, "cup", 4.25),
    "Artisan Bread Topping": ConversionContext(0.25, "cup", 1.5),
    "Baker's Cinnamon Filling": ConversionContext(1.0, "cup", 5.375),
    "Baker's Fruit Blend": ConversionContext(1.0, "cup", 4.5),
    "Baker's Special Sugar (superfine sugar, castor sugar)": ConversionContext(
        1.0, "cup", 6.75
    ),
    "Baking powder": ConversionContext(1.0, "teaspoon", 0.1410958),
    "Baking soda": ConversionContext(0.5, "teaspoon", 0.1058219),
    "Baking Sugar Alternative": ConversionContext(1.0, "cup", 6.0),
    "Bananas (mashed)": ConversionContext(1.0, "cup", 8.0),
    "Barley (cooked)": ConversionContext(1.0, "cup", 7.625),
    "Barley (pearled)": ConversionContext(1.0, "cup", 7.5),
    "Barley flakes": ConversionContext(0.5, "cup", 1.625),
    "Barley flour": ConversionContext(1.0, "cup", 3.0),
    "Barley malt syrup": ConversionContext(2.0, "tablespoons", 1.5),
    "Basil pesto": ConversionContext(2.0, "tablespoons", 1.0),
    "Bell peppers (fresh)": ConversionContext(1.0, "cup", 5.0),
    "Berries (frozen)": ConversionContext(1.0, "cup", 5.0),
    "Blueberries (dried)": ConversionContext(1.0, "cup", 5.5),
    "Blueberries (fresh)": ConversionContext(1.0, "cup", 6.0),
    "Blueberry juice": ConversionContext(1.0, "cup", 8.5),
    "Boiled cider": ConversionContext(0.25, "cup", 3.0),
    "Bran cereal": ConversionContext(1.0, "cup", 2.125),
    "Bread crumbs (dried)": ConversionContext(0.25, "cup", 1.0),
    "Bread crumbs (fresh)": ConversionContext(0.25, "cup", 0.75),
    "Bread crumbs (Japanese Panko)": ConversionContext(1.0, "cup", 1.75),
    "Bread Flour": ConversionContext(1.0, "cup", 4.25),
    "Brown rice (cooked)": ConversionContext(1.0, "cup", 6.0),
    "Brown rice flour": ConversionContext(1.0, "cup", 4.5),
    "Brown sugar (dark or light, packed)": ConversionContext(1.0, "cup", 7.5),
    "Buckwheat (whole)": ConversionContext(1.0, "cup", 6.0),
    "Buckwheat Flour": ConversionContext(1.0, "cup", 4.25),
    "Bulgur": ConversionContext(1.0, "cup", 5.375),
    "Butter": ConversionContext(8.0, "tablespoons", 4.0),
    "Buttermilk": ConversionContext(1.0, "cup", 8.0),
    "Buttermilk powder": ConversionContext(2.0, "tablespoons", 0.6666666666666666),
    "Cacao nibs": ConversionContext(1.0, "cup", 4.25),
    "Cake Enhancer": ConversionContext(2.0, "tablespoons", 0.5),
    "Candied peel": ConversionContext(0.5, "cup", 3.0),
    "Caramel (14-16 individual pieces, 1in squares)": ConversionContext(
        0.5, "cup", 5.0
    ),
    "Caramel bits (chopped Heath or toffee)": ConversionContext(1.0, "cup", 5.5),
    "Caraway seeds": ConversionContext(2.0, "tablespoons", 0.625),
    "Carrots (cooked and puréed)": ConversionContext(0.5, "cup", 4.5),
    "Carrots (diced)": ConversionContext(1.0, "cup", 5.0),
    "Carrots (grated)": ConversionContext(1.0, "cup", 3.5),
    "Cashews (chopped)": ConversionContext(1.0, "cup", 4.0),
    "Cashews (whole)": ConversionContext(1.0, "cup", 4.0),
    "Celery (diced)": ConversionContext(1.0, "cup", 5.0),
    "Cheese (Feta)": ConversionContext(0.5, "cup", 2.0),
    "Cheese (grated cheddar, jack, mozzarella, or Swiss)": ConversionContext(
        1.0, "cup", 4.0
    ),
    "Cheese (grated Parmesan)": ConversionContext(0.5, "cup", 1.75),
    "Cheese (Ricotta)": ConversionContext(1.0, "cup", 8.0),
    "Cherries (candied)": ConversionContext(0.25, "cup", 1.75),
    "Cherries (dried)": ConversionContext(0.5, "cup", 2.5),
    "Cherries (fresh, pitted, chopped)": ConversionContext(0.5, "cup", 2.875),
    "Cherries (frozen)": ConversionContext(1.0, "cup", 4.0),
    "Cherry Concentrate": ConversionContext(2.0, "tablespoons", 1.5),
    "Chickpea flour": ConversionContext(1.0, "cup", 3.0),
    "Chives (fresh)": ConversionContext(0.5, "cup", 0.75),
    "Chocolate (chopped)": ConversionContext(1.0, "cup", 6.0),
    "Chocolate Chips": ConversionContext(1.0, "cup", 6.0),
    "Chocolate Chunks": ConversionContext(1.0, "cup", 6.0),
    "Cinnamon Sweet Bits": ConversionContext(1.0, "cup", 5.0),
    "Cinnamon-Sugar": ConversionContext(0.25, "cup", 1.75),
    "Cocoa (unsweetened)": ConversionContext(0.5, "cup", 1.5),
    "Coconut (sweetened, shredded)": ConversionContext(1.0, "cup", 3.0),
    "Coconut (toasted)": ConversionContext(1.0, "cup", 3.0),
    "Coconut (unsweetened, desiccated)": ConversionContext(1.0, "cup", 3.0),
    "Coconut (unsweetened, large flakes)": ConversionContext(1.0, "cup", 2.125),
    "Coconut (unsweetened, shredded)": ConversionContext(1.0, "cup", 1.875),
    "Coconut Flour": ConversionContext(1.0, "cup", 4.5),
    "Coconut Milk Powder": ConversionContext(0.5, "cup", 2.0),
    "Coconut oil": ConversionContext(0.5, "cup", 4.0),
    "Coconut sugar": ConversionContext(0.5, "cup", 2.75),
    "Confectioners' sugar (unsifted)": ConversionContext(2.0, "cups", 8.0),
    "Cookie crumbs": ConversionContext(1.0, "cup", 3.0),
    "Corn (popped)": ConversionContext(4.0, "cups", 0.75),
    "Corn syrup": ConversionContext(1.0, "cup", 11.0),
    "Cornmeal (whole)": ConversionContext(1.0, "cup", 4.875),
    "Cornmeal (yellow, Quaker)": ConversionContext(1.0, "cup", 5.5),
    "Cornstarch": ConversionContext(0.25, "cup", 1.0),
    "Cracked wheat": ConversionContext(1.0, "cup", 5.25),
    "Cranberries (dried)": ConversionContext(0.5, "cup", 2.0),
    "Cranberries (fresh or frozen)": ConversionContext(1.0, "cup", 3.5),
    "Cream (heavy cream, light cream, or half & half)": ConversionContext(
        1.0, "cup", 8.0
    ),
    "Cream cheese": ConversionContext(1.0, "cup", 8.0),
    "Crystallized ginger": ConversionContext(0.5, "cup", 3.25),
    "Currants": ConversionContext(1.0, "cup", 5.0),
    "Dates (chopped)": ConversionContext(1.0, "cup", 5.25),
    "Demerara sugar": ConversionContext(1.0, "cup", 7.75),
    "Dried Blueberry Powder": ConversionContext(0.25, "cup", 1.0),
    "Dried milk (Baker's Special Dry Milk)": ConversionContext(0.25, "cup", 1.0),
    "Dried nonfat milk (powdered)": ConversionContext(0.25, "cup", 1.0),
    "Dried potato flakes (instant mashed potatoes)": ConversionContext(0.5, "cup", 1.5),
    "Dried whole milk (powdered)": ConversionContext(0.5, "cup", 1.75),
    "Durum Flour": ConversionContext(1.0, "cup", 4.375),
    "Easy Roll Dough Improver": ConversionContext(2.0, "tablespoons", 0.625),
    "Egg (fresh)": ConversionContext(1.0, "large", 1.75),
    "Egg white (fresh)": ConversionContext(1.0, "large", 1.25),
    "Egg whites (dried)": ConversionContext(2.0, "tablespoons", 0.375),
    "Egg yolk (fresh)": ConversionContext(1.0, "large", 0.5),
    "Espresso Powder": ConversionContext(1.0, "tablespoon", 0.25),
    "Everything Bagel Topping": ConversionContext(0.25, "cup", 1.25),
    "Figs (dried, chopped)": ConversionContext(1.0, "cup", 5.25),
    "First Clear Flour": ConversionContext(1.0, "cup", 3.75),
    "Flax meal": ConversionContext(0.5, "cup", 1.75),
    "Flaxseed": ConversionContext(0.25, "cup", 1.25),
    "French-Style Flour": ConversionContext(1.0, "cup", 4.25),
    "Fruitcake Fruit Blend": ConversionContext(1.0, "cup", 4.25),
    "Garlic (cloves, in skin for roasting)": ConversionContext(1.0, "large", 4.0),
    "Garlic (minced)": ConversionContext(2.0, "tablespoons", 1.0),
    "Garlic (peeled and sliced)": ConversionContext(1.0, "cup", 5.25),
    "Ginger (fresh, sliced)": ConversionContext(0.25, "cup", 2.0),
    "Gluten-Free All-Purpose Baking Mix": ConversionContext(1.0, "cup", 4.25),
    "Gluten-Free All-Purpose Flour": ConversionContext(1.0, "cup", 5.5),
    "Gluten-Free Measure for Measure Flour": ConversionContext(1.0, "cup", 4.25),
    "Graham cracker crumbs (boxed)": ConversionContext(1.0, "cup", 3.5),
    "Graham crackers (crushed)": ConversionContext(1.0, "cup", 5.0),
    "Granola": ConversionContext(1.0, "cup", 4.0),
    "Grape Nuts": ConversionContext(0.5, "cup", 2.0),
    "Harvest Grains Blend": ConversionContext(0.5, "cup", 2.625),
    "Hazelnut flour": ConversionContext(1.0, "cup", 3.125),
    "Hazelnut Praline Paste": ConversionContext(0.5, "cup", 5.5),
    "Hazelnut spread": ConversionContext(0.5, "cup", 5.625),
    "Hazelnuts (whole)": ConversionContext(1.0, "cup", 5.0),
    "Hi-Maize Natural Fiber": ConversionContext(0.25, "cup", 1.125),
    "High-Gluten Flour": ConversionContext(1.0, "cup", 4.25),
    "Honey": ConversionContext(1.0, "tablespoon", 0.75),
    "Instant ClearJel": ConversionContext(1.0, "tablespoon", 0.375),
    "Irish-Style Flour": ConversionContext(1.0, "cup", 3.875),
    "Italian-Style Flour": ConversionContext(1.0, "cup", 3.75),
    "Jam or preserves": ConversionContext(0.25, "cup", 3.0),
    "Jammy Bits": ConversionContext(1.0, "cup", 6.5),
    "Keto Wheat Flour": ConversionContext(1.0, "cup", 4.25),
    "Key Lime Juice": ConversionContext(1.0, "cup", 8.0),
    "Lard": ConversionContext(0.5, "cup", 4.0),
    "Leeks (diced)": ConversionContext(1.0, "cup", 3.25),
    "Lemon Juice Powder": ConversionContext(2.0, "tablespoons", 0.625),
    "Lime Juice Powder": ConversionContext(2.0, "tablespoons", 0.625),
    "Macadamia nuts (whole)": ConversionContext(1.0, "cup", 5.25),
    "Malt syrup": ConversionContext(2.0, "tablespoons", 1.5),
    "Malted Milk Powder": ConversionContext(0.25, "cup", 1.25),
    "Malted Wheat Flakes": ConversionContext(0.5, "cup", 2.25),
    "Maple sugar": ConversionContext(0.5, "cup", 2.75),
    "Maple syrup": ConversionContext(0.5, "cup", 5.5),
    "Marshmallow crème": ConversionContext(1.0, "cup", 3.0),
    "Marshmallow Fluff®": ConversionContext(1.0, "cup", 4.5),
    "Marshmallows (mini)": ConversionContext(1.0, "cup", 1.5),
    "Marzipan": ConversionContext(1.0, "cup", 10.125),
    "Mascarpone cheese": ConversionContext(1.0, "cup", 8.0),
    "Mashed potatoes": ConversionContext(1.0, "cup", 7.5),
    "Mayonnaise": ConversionContext(0.5, "cup", 4.0),
    "Medium Rye Flour": ConversionContext(1.0, "cup", 3.75),
    "Meringue powder": ConversionContext(0.25, "cup", 1.5),
    "Milk (evaporated)": ConversionContext(0.5, "cup", 4.0),
    "Milk (fresh)": ConversionContext(1.0, "cup", 8.0),
    "Millet (whole)": ConversionContext(0.5, "cup", 3.625),
    "Mini chocolate chips": ConversionContext(1.0, "cup", 6.25),
    "Molasses": ConversionContext(0.25, "cup", 3.0),
    "Mushrooms (sliced)": ConversionContext(1.0, "cup", 2.75),
    "Non-Diastatic Malt Powder": ConversionContext(2.0, "tablespoons", 0.625),
    "Oat bran": ConversionContext(0.5, "cup", 1.875),
    "Oat flour": ConversionContext(1.0, "cup", 3.25),
    "Oats (old-fashioned or quick-cooking)": ConversionContext(1.0, "cup", 3.125),
    "Olive oil": ConversionContext(0.25, "cup", 1.75),
    "Olives (sliced)": ConversionContext(1.0, "cup", 5.0),
    "Onions (fresh, diced)": ConversionContext(1.0, "cup", 5.0),
    "Paleo Baking Flour": ConversionContext(1.0, "cup", 3.625),
    "Palm shortening": ConversionContext(0.25, "cup", 1.5),
    "Passion fruit purée ": ConversionContext(0.3333333333333333, "cup", 2.125),
    "Pasta Flour Blend": ConversionContext(1.0, "cup", 5.125),
    "Pastry Flour": ConversionContext(1.0, "cup", 3.75),
    "Pastry Flour Blend": ConversionContext(1.0, "cup", 4.0),
    "Peaches (peeled and diced)": ConversionContext(1.0, "cup", 6.0),
    "Peanut butter": ConversionContext(0.5, "cup", 4.75),
    "Peanuts (whole, shelled)": ConversionContext(1.0, "cup", 5.0),
    "Pears (peeled and diced)": ConversionContext(1.0, "cup", 5.75),
    "Pecan Meal": ConversionContext(1.0, "cup", 2.75),
    "Pecans (diced)": ConversionContext(0.5, "cup", 2.0),
    "Pie Filling Enhancer": ConversionContext(0.25, "cup", 1.625),
    "Pine nuts": ConversionContext(0.5, "cup", 2.5),
    "Pineapple (dried)": ConversionContext(0.5, "cup", 2.5),
    "Pineapple (fresh or canned, diced)": ConversionContext(1.0, "cup", 6.0),
    "Pistachio nuts (shelled)": ConversionContext(0.5, "cup", 2.125),
    "Pistachio Paste": ConversionContext(0.25, "cup", 2.75),
    "Pizza Dough Flavor": ConversionContext(2.0, "tablespoons", 0.4232875),
    "Pizza Flour": ConversionContext(1.0, "cup", 4.0),
    "Pizza Flour Blend": ConversionContext(1.0, "cup", 4.375),
    "Polenta (coarse ground cornmeal)": ConversionContext(1.0, "cup", 5.75),
    "Poppy seeds": ConversionContext(2.0, "tablespoons", 0.625),
    "Potato Flour": ConversionContext(0.25, "cup", 1.625),
    "Potato starch": ConversionContext(1.0, "cup", 5.375),
    "Pumpernickel Flour": ConversionContext(1.0, "cup", 3.75),
    "Pumpkin purée ": ConversionContext(1.0, "cup", 8.0),
    "Quinoa (cooked)": ConversionContext(1.0, "cup", 6.5),
    "Quinoa (whole)": ConversionContext(1.0, "cup", 6.25),
    "Quinoa flour": ConversionContext(1.0, "cup", 3.875),
    "Raisins (loose)": ConversionContext(1.0, "cup", 5.25),
    "Raisins (packed)": ConversionContext(0.5, "cup", 3.0),
    "Raspberries (fresh)": ConversionContext(1.0, "cup", 4.25),
    "Rhubarb (sliced, 1/2in slices)": ConversionContext(1.0, "cup", 4.25),
    "Rice (long grain, dry)": ConversionContext(0.5, "cup", 3.5),
    "Rice flour (white)": ConversionContext(1.0, "cup", 5.0),
    "Rice Krispies": ConversionContext(1.0, "cup", 1.0),
    "Rye Bread Improver": ConversionContext(2.0, "tablespoons", 0.4938355),
    "Rye Chops": ConversionContext(1.0, "cup", 4.25),
    "Rye flakes": ConversionContext(1.0, "cup", 4.375),
    "Rye Flour Blend": ConversionContext(1.0, "cup", 3.75),
    "Salt (Kosher, Diamond Crystal)": ConversionContext(1.0, "tablespoon", 0.2821917),
    "Salt (Kosher, Morton's)": ConversionContext(1.0, "tablespoon", 0.5643834),
    "Salt (table)": ConversionContext(1.0, "tablespoon", 0.6349313),
    "Scallions (sliced)": ConversionContext(1.0, "cup", 2.25),
    "Self-Rising Flour": ConversionContext(1.0, "cup", 4.0),
    "Semolina Flour": ConversionContext(1.0, "cup", 5.75),
    "Sesame seeds": ConversionContext(0.5, "cup", 2.5),
    "Shallots (peeled and sliced)": ConversionContext(1.0, "cup", 5.5),
    "Six-Grain Blend": ConversionContext(1.0, "cup", 4.5),
    "Sorghum flour": ConversionContext(1.0, "cup", 4.875),
    "Sour cream": ConversionContext(1.0, "cup", 8.0),
    "Sourdough starter": ConversionContext(1.0, "cup", 8.25),
    "Soy flour": ConversionContext(0.25, "cup", 1.25),
    "Sparkling Sugar": ConversionContext(0.25, "cup", 2.0),
    "Spelt Flour": ConversionContext(1.0, "cup", 3.5),
    "Sprouted Wheat Flour": ConversionContext(1.0, "cup", 4.0),
    "Steel cut oats": ConversionContext(0.5, "cup", 2.5),
    "Sticky Bun Sugar": ConversionContext(1.0, "cup", 3.5),
    "Strawberries (fresh sliced)": ConversionContext(1.0, "cup", 5.875),
    "Sugar (granulated white)": ConversionContext(1.0, "cup", 7.0),
    "Sugar substitute (Splenda)": ConversionContext(1.0, "cup", 0.875),
    "Sundried tomatoes (dry pack)": ConversionContext(1.0, "cup", 6.0),
    "Sunflower seeds": ConversionContext(0.25, "cup", 1.25),
    "Super 10 Blend": ConversionContext(1.0, "cup", 3.75),
    "Sweet Ground Chocolate and Cocoa Blend": ConversionContext(0.25, "cup", 1.0),
    "Sweetened condensed milk": ConversionContext(0.25, "cup", 2.75),
    "Tahini paste": ConversionContext(0.5, "cup", 4.5),
    "Tapioca starch or flour": ConversionContext(1.0, "cup", 4.0),
    "Tapioca (quick cooking)": ConversionContext(2.0, "tablespoons", 0.75),
    "Teff flour": ConversionContext(1.0, "cup", 4.75),
    "The Works Bread Topping": ConversionContext(0.25, "cup", 1.25),
    "Toasted Almond Flour": ConversionContext(1.0, "cup", 3.375),
    "Toffee chunks": ConversionContext(1.0, "cup", 5.5),
    "Tropical Fruit Blend": ConversionContext(1.0, "cup", 4.75),
    "Turbinado sugar (raw)": ConversionContext(1.0, "cup", 6.375),
    "Unbleached Cake Flour": ConversionContext(1.0, "cup", 4.25),
    "Vanilla Extract ": ConversionContext(1.0, "tablespoon", 0.5),
    "Vegetable oil": ConversionContext(1.0, "cup", 7.0),
    "Vegetable shortening": ConversionContext(0.25, "cup", 1.625),
    "Vermont Cheese Powder": ConversionContext(0.5, "cup", 2.0),
    "Vital Wheat Gluten": ConversionContext(2.0, "tablespoons", 0.625),
    "Walnuts (chopped)": ConversionContext(1.0, "cup", 4.0),
    "Walnuts (whole)": ConversionContext(0.5, "cup", 2.25),
    "Wheat berries (red)": ConversionContext(1.0, "cup", 6.5),
    "Wheat bran": ConversionContext(0.5, "cup", 1.125),
    "Wheat germ": ConversionContext(0.25, "cup", 1.0),
    "White Chocolate Chips": ConversionContext(1.0, "cup", 6.0),
    "White Rye Flour": ConversionContext(1.0, "cup", 3.75),
    "White Whole Wheat Flour": ConversionContext(1.0, "cup", 4.0),
    "Whole Grain Flour Blend": ConversionContext(1.0, "cup", 4.0),
    "Whole Wheat Flour (Premium 100%)": ConversionContext(1.0, "cup", 4.0),
    "Whole Wheat Pastry Flour / Graham Flour": ConversionContext(1.0, "cup", 3.375),
    "Yeast (instant)": ConversionContext(1.0, "tablespoon", 0.3333333333333333),
    "Yogurt": ConversionContext(1.0, "cup", 8.0),
    "Zucchini (shredded)": ConversionContext(1.0, "cup", 4.75),
}

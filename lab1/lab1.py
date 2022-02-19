import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Solution:
    def __init__(self) -> None:
        # Load data from data/chipotle.tsv file using Pandas library and 
        # assign the dataset to the 'chipo' variable.
        file = 'data/chipotle.tsv'
        self.chipo = pd.read_csv(file, '\t')
    
    def top_x(self, count) -> None:
        # Top x number of entries from the dataset and display as markdown format.
        topx = self.chipo.head(count)
        print(topx.to_markdown())
        
    def count(self) -> int:
        # The number of observations/entries in the dataset.
        return self.chipo.shape[0]
    
    def info(self) -> None:
        # print data info.
        print(self.chipo.info())
    
    def num_column(self) -> int:
        # return the number of columns in the dataset
        return self.chipo.shape[1]
    
    def print_columns(self) -> None:
        # Print the name of all the columns.
        print(self.chipo.columns)
    
    def most_ordered_item(self):
        most_ordered_item = self.chipo.groupby(['item_name'], as_index=False).sum('quantity').sort_values(['quantity'], ascending=False).head(1)
        item_name = most_ordered_item.iloc[0]['item_name']
        order_id = most_ordered_item.iloc[0]['order_id']
        quantity = most_ordered_item.iloc[0]['quantity']
        return item_name, order_id, quantity

    def total_item_orders(self) -> int:
       # How many items were orderd in total?
       return self.chipo.quantity.sum()
   
    def total_sales(self) -> float:
        # 1. Create a lambda function to change all item prices to float.
        #self.chipo['item_price'] = self.chipo.item_price.map(lambda x: float(x[1:]))
        price = self.chipo['item_price'].apply(lambda x: x.replace('$', '')if isinstance(x, str) else x).astype(float)
        # 2. Calculate total sales.
        return (self.chipo['quantity'] * price).sum()
   
    def num_orders(self) -> int:
        # How many orders were made in the dataset?
        return self.chipo.order_id.value_counts().count()
    
    def average_sales_amount_per_order(self) -> float:
        #self.chipo['sales'] = self.chipo.quantity * self.chipo.item_price
        #avg_sales = self.chipo.groupby(['order_id']).sum().mean()['sales']
        avg_sales = self.total_sales() / self.num_orders()
        return round(avg_sales, 2)

    def num_different_items_sold(self) -> int:
        # How many different items are sold?
        items_sold = self.chipo.item_name.value_counts().count()
        #self.chipo.item_name.nunique()
        return items_sold
    
    def plot_histogram_top_x_popular_items(self, x:int) -> None:
        from collections import Counter
        letter_counter = Counter(self.chipo.item_name)
        # 1. convert the dictionary to a DataFrame
        df = pd.DataFrame(list(letter_counter.items()), columns=['item_name','orders'])
        # 2. sort the values from the top to the least value and slice the first 5 items
        most_ordered_items = df.sort_values(['orders'], ascending=False).head(5)
        # 3. create a 'bar' plot from the DataFrame
        plt.bar(most_ordered_items['item_name'], most_ordered_items['orders'])
        #plt.subplots_adjust(right=1.2)
        #most_ordered_items.plot.bar(x = 'items', y = 'orders', title='Most Popular Items', fontsize='9')
        # 4. set the title and labels:
        #     x: Items
        #     y: Number of Orders
        #     title: Most popular items
        plt.xlabel('Items')
        plt.ylabel('Orders')
        plt.title('Most Popular Items')
        # 5. show the plot. Hint: plt.show(block=True).
        plt.show(block=True)
        
    def scatter_plot_num_items_per_order_price(self) -> None:
        # 1. create a list of prices by removing dollar sign and trailing space.
        self.chipo['item_price'] = self.chipo['item_price'].replace({"\$": ""}, regex= True).str.strip().astype(float)
        list_of_prices = list(self.chipo['item_price'])
        
        # 2. groupby the orders and sum it.
        orders = self.chipo.groupby('order_id').sum()
        
        # 3. create a scatter plot:
        #       x: orders' item price
        #       y: orders' quantity
        #       s: 50
        #       c: blue
        plt.scatter(x = orders.item_price, y = orders.quantity, s = 50, c = 'blue')

        # 4. set the title and labels.
        #       title: Number of items per order price
        #       x: Order Price
        #       y: Num Items
        plt.xlabel('Order Price')
        plt.ylabel('Num Items')
        plt.title('Number of items per order price')
        plt.ylim(0)
        plt.show()
    
        

def test() -> None:
    solution = Solution()
    solution.top_x(10)
    count = solution.count()
    print(count)
    assert count == 4622
    solution.info()
    count = solution.num_column()
    assert count == 5
    item_name, order_id, quantity = solution.most_ordered_item()
    assert item_name == 'Chicken Bowl'
    assert order_id == 713926	
    assert quantity == 761
    total = solution.total_item_orders()
    assert total == 4972
    assert 39237.02 == solution.total_sales()
    assert 1834 == solution.num_orders()
    assert 21.39 == solution.average_sales_amount_per_order()
    assert 50 == solution.num_different_items_sold()
    solution.plot_histogram_top_x_popular_items(5)
    solution.scatter_plot_num_items_per_order_price()

    
if __name__ == "__main__":
    # execute only if run as a script
    test()
    
    
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pprint

# get each run of vivaldiUpdate
raw_data = open("coordinate_table.txt", "r").read().strip('\n').split('*')

# list of list(state at each call to vivaldi) of tuples(hostname, x, y)
data = []

# clean up 
for block in raw_data:
    if len(block) > 1:
        coordinate_table_state = [] 
    
        block_contents = block.strip().split('\n')

        for row in block_contents:
            if len(row) > 1:
                hostname, x, y = row.split('|')
                row = (hostname.strip(), float(x), float(y))
                coordinate_table_state.append(row)

        data.append(coordinate_table_state)

# reverse so i can pop off in the right order
data.reverse()

# hold the number of updates
size = len(data)

# plotting 
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
plt.subplots_adjust(bottom=0.1)

colors = [i for i in range(len(data[0]))]

print(" Plotting {} Snapshots".format(len(data)))
print("-------------------------")

def animate(i):
    ax1.clear()
    current_run = data.pop()

    # output what is currently being plotted
    pp = pprint.PrettyPrinter(indent=2) 
    print("\ncoordinate table at snapshot: {}".format(size - len(data)))
    print("---------------------------------------")

    pp.pprint(current_run)

    hostnames, xvals, yvals = zip(*current_run)

    # set up the labels
    for host, x, y in zip(hostnames, xvals, yvals):
        plt.annotate(host, xy=(x,y), xytext=(10,10),
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='grey', alpha=0.5))

    plt.scatter(xvals, yvals, marker='o', c=colors, cmap=plt.get_cmap('Spectral'))


# run the animation, refreshes at interval milliseconds, runs for frames, and stops on the last frame
ani = animation.FuncAnimation(fig, animate, interval=2000, frames=len(data)-1, repeat=False)
plt.show()

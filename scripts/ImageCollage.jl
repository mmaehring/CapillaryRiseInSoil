using Plots
using Images, FileIO

cd("C:\\Users\\marcu\\OneDrive\\Desktop\\PraktikumIII\\CapillaryRiseInSoil")
path = "processed_data"

searchdir(path,key) = filter(x->contains(x,key), readdir(path))
images = searchdir(path, ".png")

img = load.([path*'/'*images[i] for i in 1:length(images)])

l = @layout grid(2,3)


plt1 = plot(img[1])
plt2 = plot(img[2])
plt3 = plot(img[3])
plt4 = plot(img[4])
plt5 = plot(img[5])
plt6 = plot(img[5])

plot(plt1, plt2, plt3, plt4, plt5, plt6, layout = l)

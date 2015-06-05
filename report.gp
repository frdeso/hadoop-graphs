set term png dashlength 1 size 1920,2080
set datafile separator ","
set output "report.png"
set key inside top center
TOP=0.98
SPLIT=0.05
DY = 0.14
set grid xtics mxtics
set xlabel "Time [s]"
set ylabel "kB/s [s]"
set yrange  [0:130000]
set lmargin at screen 0.05
set multiplot layout 2,1 rowsfirst title name

set tmargin at screen TOP
set bmargin at screen TOP-DY
plot data using (5*$0):2 with linespoints title 'Disk read', \
		 data	using (5*$0):3 with linespoints  title 'Disk write', \
		 120000 lt 0 lw 1 lc rgb "red" title 'Read limit 120 Mb/s', \
		 100000 lt 0 lw 1 lc rgb "green" title 'Write limit 100 Mb/s'

set tmargin at screen TOP-DY-SPLIT
set bmargin at screen TOP-2*DY-SPLIT
set yrange  [0:100]
set ylabel "Disk Utilization [%]"
plot 	 data	using (5*$0):4 with linespoints  title 'DisK utilization' lc rgb "blue" 

set tmargin at screen TOP-2*DY-2*SPLIT
set bmargin at screen TOP-3*DY-2*SPLIT
set yrange  [0:100]
set ylabel "CPU Usage [%]"
plot 	 data	using (5*$0):1 with linespoints  title 'CPU usage' lc rgb "purple", \
		 	9 lt 0 lw 1 lc rgb "red" title '3 cores' 

set tmargin at screen TOP-3*DY-3*SPLIT
set bmargin at screen TOP-4*DY-3*SPLIT
set yrange [0:7000000]
set ylabel "Mem Usage [KB]"
plot 	data	using (5*$0):5 with linespoints  title 'Memory usage' lc rgb "orange"

set tmargin at screen TOP-4*DY-4*SPLIT
set bmargin at screen TOP-5*DY-4*SPLIT
unset ytics
unset key
unset ylabel

set yrange  [0:10]
load "rect.gp"
#Line type to -3 to be the same as the background color
plot data using (5*$0):3 with lines linewidth 1 linetype -3
unset multiplot

lttng destroy -a
lttng create allo
lttng add-context --kernel --type vtid --type procname --type vpid
lttng enable-event -k --syscall read
lttng enable-event -k --syscall open
lttng enable-event -k --syscall close
lttng enable-event -k --syscall execve
lttng enable-event -k --syscall exit
lttng enable-event -k --tracepoint sched_process_fork
lttng enable-event -k --tracepoint sched_switch
lttng start
sleep 1
lttng stop


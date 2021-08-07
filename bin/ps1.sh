#!/bin/sh

BATTERY="$(acpi | awk '{print $4}')";
BATTERY="${BATTERY%%,}"
MEMFREE="$(free --mega | head -n2 | tail -n1 | awk '{print $4 "/" $2}')"
SWAPFREE="$(free --mega | awk '{print "/" $3}' | tail -n1)"
THERM="$(acpi --thermal | awk '{print $4}' | head -n1)C"
AC="$(acpi | grep 'Discharging')"

BATTERY_COLOR=10
MEMFREE_COLOR=12
SWAPFREE_COLOR=9
THERM_COLOR=6

if [ -n "$AC" ]; then
   BATTERY_COLOR=15
fi

if [[ "$(whoami)" = "root" ]]; then 
   BATTERY_COLOR=15
   MEMFREE_COLOR=15
   SWAPFREE_COLOR=15
   THERM_COLOR=15
fi

# echo "$(tput setf $BATTERY_COLOR)${BATTERY}$(tput sgr0)|$(tput setf $MEMFREE_COLOR)${MEMFREE}$(tput setf $SWAPFREE_COLOR)${SWAPFREE}$(tput sgr0)|$(tput setf $THERM_COLOR)${THERM}$(tput sgr0)"
echo "${BATTERY}|${MEMFREE}${SWAPFREE}|${THERM}"


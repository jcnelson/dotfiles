#!/bin/bash

for cmd in curl jq sed bc; do
   which $cmd >/dev/null 2>&1 || ( echo >&2 "Missing command $cmd"; exit 1 )
done

host="$1"
if [ -z "$host" ]; then
   #host="seed-0.mainnet.stacks.co:20443"
   host="52.0.54.100:20443"
fi

set -ueo pipefail

# pox info
pox_info="$(curl -sf http://$host/v2/pox)"

# which reward cycle are we in?
cur_reward_cycle="$(echo "$pox_info" | jq -r '.reward_cycle_id')"
next_reward_cycle="$((cur_reward_cycle + 1))"

# call read-only get-total-ustx-stacked
next_reward_cycle_clarity_value="$(printf "0x01%032x" "$next_reward_cycle")"
body="{
   \"sender\": \"SP31DA6FTSJX2WGTZ69SFY11BH51NZMB0ZW97B5P0.get-info\",
   \"arguments\": [
        \"$next_reward_cycle_clarity_value\"
   ] 
}"

body_len=${#body}

ustx_hex="$(echo "$body" | curl -sf -X POST -H "content-type: application/json" -H "content-length: $body_len" --data-binary @- "http://$host/v2/contracts/call-read/SP000000000000000000002Q6VF78/pox/get-total-ustx-stacked" | \
        jq -r '.result' | \
        sed -r 's/0x010*//g')"

# how many uSTX are participating
participation="$(printf "%d" $((16#$ustx_hex)))"

# calculate min uSTX per lockup
pox_maximal_scaling=4
reward_slots=4000
ustx_step=$((10000 * 1000000))
liquid_ustx="$(echo "$pox_info" | jq -r '.total_liquid_supply_ustx')"
time_to_next_reward_cycle="$(echo "$pox_info" | jq -r '.next_reward_cycle_in')"

scale_by=0
if (( $participation > $liquid_ustx / $pox_maximal_scaling )); then
   scale_by=$participation
else
   scale_by=$((liquid_ustx / pox_maximal_scaling))
fi

threshold_precise=$((scale_by / reward_slots))

ceil_amount=0
if (( $threshold_precise % $ustx_step != 0 )); then
   ceil_amount=$(($ustx_step - threshold_precise % $ustx_step))
fi

threshold_ustx=$((threshold_precise + ceil_amount))

echo -n "STX locked: "
echo "scale=6; $participation / 1000000" | bc

echo "Next reward cycle: $next_reward_cycle"

echo -n "Fraction of STX participating: "
echo "scale=4; $participation * 100 / $liquid_ustx" | bc

echo -n "Minimum STX per reward address: "
echo "scale=6; $threshold_ustx / 1000000" | bc

echo -n "STX/reward-address until the next minimum: "
echo "scale=6; $ceil_amount / 1000000" | bc

printf "Blocks to next reward cycle: %d\n" $time_to_next_reward_cycle

exit 0


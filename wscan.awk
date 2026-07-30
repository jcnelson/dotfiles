#!/usr/bin/gawk

/^BSS/ {
   MAC = gensub(/^(.+)\(on$/, "\\1", "g", $2)
   wifi[MAC]["mac"] = MAC
   wifi[MAC]["enc"] = "Open"
}
$1 == "SSID:" {
   $1 = ""
   wifi[MAC]["SSID"] = $0
}
$1 == "freq:" {
   wifi[MAC]["freq"] = $NF
}
$1 == "signal:" {
   wifi[MAC]["sig"] = $2 " " $3
}
$1 == "WPA:" {
   wifi[MAC]["enc"] = "WPA"
}
$1 == "WEP:" {
   wifi[MAC]["enc"] = "WEP"
}
END {
   printf "%-17s\t%-20s\t%-15s\t%-15s\t%-5s\n", "MAC", "SSID", "Frequency", "Signal", "Encryption"

   for (w in wifi) {
      printf "%-17s\t%-20s\t%-15s\t%-15s\t%-5s\n", wifi[w]["mac"], wifi[w]["SSID"], wifi[w]["freq"], wifi[w]["sig"], wifi[w]["enc"]
   }
}

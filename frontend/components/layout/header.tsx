"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Badge } from "@/components/ui/badge"
import { useWeb3 } from "@/components/providers/web3-provider"
import { Shield, Menu, LogOut } from "lucide-react"
import { cn } from "@/lib/utils"

const navigation = [
  { name: "Home", href: "/" },
  { name: "Dashboard", href: "/dashboard" },
  { name: "Query", href: "/query" },
  { name: "Admin", href: "/admin" },
  { name: "Learn", href: "/learn" },
]

export function Header() {
  const pathname = usePathname()
  const { account, isConnected, isConnecting, connect, disconnect } = useWeb3()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <Shield className="h-6 w-6 text-primary" />
            <span className="font-bold text-xl">AutoShield</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "text-sm font-medium transition-colors hover:text-primary",
                  pathname === item.href ? "text-primary" : "text-muted-foreground",
                )}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Wallet Connection */}
          <div className="flex items-center space-x-4">
            {isConnected ? (
              <div className="flex items-center space-x-2">
                <Badge variant="outline" className="hidden sm:flex">
                  {account?.slice(0, 6)}...{account?.slice(-4)}
                </Badge>
                <Button variant="outline" size="sm" onClick={disconnect} className="hidden sm:flex bg-transparent">
                  <LogOut className="h-4 w-4 mr-2" />
                  Disconnect
                </Button>
              </div>
            ) : (
              <Button onClick={connect} disabled={isConnecting} className="hidden sm:flex">
                {isConnecting ? "Connecting..." : "Connect Wallet"}
              </Button>
            )}

            {/* Mobile Menu */}
            <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="sm" className="md:hidden">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-[300px]">
                <div className="flex flex-col space-y-4 mt-8">
                  {navigation.map((item) => (
                    <Link
                      key={item.name}
                      href={item.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={cn(
                        "text-sm font-medium transition-colors hover:text-primary px-2 py-1",
                        pathname === item.href ? "text-primary" : "text-muted-foreground",
                      )}
                    >
                      {item.name}
                    </Link>
                  ))}

                  <div className="border-t pt-4">
                    {isConnected ? (
                      <div className="space-y-2">
                        <div className="text-sm text-muted-foreground">
                          Connected: {account?.slice(0, 6)}...{account?.slice(-4)}
                        </div>
                        <Button variant="outline" size="sm" onClick={disconnect} className="w-full bg-transparent">
                          <LogOut className="h-4 w-4 mr-2" />
                          Disconnect
                        </Button>
                      </div>
                    ) : (
                      <Button onClick={connect} disabled={isConnecting} className="w-full">
                        {isConnecting ? "Connecting..." : "Connect Wallet"}
                      </Button>
                    )}
                  </div>
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </header>
  )
}

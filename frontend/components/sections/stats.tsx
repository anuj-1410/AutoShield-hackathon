"use client"

import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"

const stats = [
  {
    value: 15847,
    label: "Accounts Verified",
    suffix: "+",
  },
  {
    value: 97.8,
    label: "Accuracy Rate",
    suffix: "%",
  },
  {
    value: 1234,
    label: "Fake Accounts Detected",
    suffix: "+",
  },
  {
    value: 50,
    label: "Fraud Reduction",
    suffix: "%",
  },
]

export function Stats() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <section className="py-24 bg-primary/5">
        <div className="container mx-auto px-4">
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
            {stats.map((_, index) => (
              <Card key={index}>
                <CardContent className="p-8 text-center">
                  <div className="h-12 bg-muted rounded animate-pulse mb-2" />
                  <div className="h-4 bg-muted rounded animate-pulse" />
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="py-24 bg-primary/5">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold mb-4">Trusted by the Web3 Community</h2>
          <p className="text-xl text-muted-foreground">Real results from our AI-powered verification system</p>
        </div>

        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat, index) => (
            <Card key={index} className="text-center">
              <CardContent className="p-8">
                <div className="text-4xl font-bold text-primary mb-2">
                  {stat.value.toLocaleString()}
                  {stat.suffix}
                </div>
                <div className="text-muted-foreground font-medium">{stat.label}</div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="mt-16 text-center">
          <p className="text-sm text-muted-foreground">Statistics updated in real-time from our global network</p>
        </div>
      </div>
    </section>
  )
}

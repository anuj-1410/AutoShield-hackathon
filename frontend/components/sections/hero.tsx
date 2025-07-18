import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Shield, ArrowRight, Zap, Lock } from "lucide-react"
import Link from "next/link"

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-background py-24 sm:py-32">
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-primary/5" />

      <div className="container mx-auto px-4 relative">
        <div className="mx-auto max-w-4xl text-center">
          <Badge variant="outline" className="mb-6">
            <Zap className="h-3 w-3 mr-1" />
            AI-Powered Web3 Security
          </Badge>

          <h1 className="text-4xl font-bold tracking-tight sm:text-6xl mb-6">
            Protect Your Web3 Ecosystem with <span className="text-primary">AutoShield</span>
          </h1>

          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Advanced AI detection combined with blockchain verification to eliminate fake accounts and reduce fraud in
            decentralized platforms by up to 80%.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Button size="lg" asChild>
              <Link href="/dashboard">
                Get Started
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link href="/learn">Learn More</Link>
            </Button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-3xl mx-auto">
            <div className="text-center">
              <div className="w-12 h-12 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="h-6 w-6 text-primary" />
              </div>
              <h3 className="font-semibold mb-2">97%+ Accuracy</h3>
              <p className="text-sm text-muted-foreground">
                Industry-leading fake account detection powered by advanced ML models
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Zap className="h-6 w-6 text-primary" />
              </div>
              <h3 className="font-semibold mb-2">Real-time Verification</h3>
              <p className="text-sm text-muted-foreground">
                Instant verification results with sub-second response times
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Lock className="h-6 w-6 text-primary" />
              </div>
              <h3 className="font-semibold mb-2">Privacy First</h3>
              <p className="text-sm text-muted-foreground">
                Zero personal data collection, only public blockchain analysis
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

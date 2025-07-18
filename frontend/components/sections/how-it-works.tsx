import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Eye, Brain, Shield, CheckCircle } from "lucide-react"

const steps = [
  {
    icon: Eye,
    title: "Data Collection",
    description:
      "Our system analyzes public blockchain data including transaction patterns, account age, interaction networks, and behavioral signals.",
    details: [
      "Transaction history analysis",
      "Network interaction patterns",
      "Account age and activity",
      "Cross-platform behavior",
    ],
  },
  {
    icon: Brain,
    title: "AI Analysis",
    description:
      "Advanced machine learning models process the collected data to identify patterns indicative of fake accounts and fraudulent behavior.",
    details: ["Pattern recognition", "Anomaly detection", "Risk scoring", "Behavioral analysis"],
  },
  {
    icon: Shield,
    title: "Cryptographic Signing",
    description:
      "Analysis results are cryptographically signed to ensure integrity and authenticity before being recorded on the blockchain.",
    details: ["Digital signatures", "Hash generation", "Integrity verification", "Tamper protection"],
  },
  {
    icon: CheckCircle,
    title: "Blockchain Storage",
    description:
      "Verification results are stored on-chain as immutable records, providing transparency and enabling public queries.",
    details: ["On-chain attestations", "Public verification", "Immutable records", "Decentralized access"],
  },
]

export function HowItWorks() {
  return (
    <section className="py-24">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <Badge variant="outline" className="mb-4">
            How It Works
          </Badge>
          <h2 className="text-3xl font-bold mb-4">Four-Step Verification Process</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Our comprehensive approach ensures accurate, transparent, and privacy-preserving account verification for
            the entire Web3 ecosystem.
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          {steps.map((step, index) => (
            <div key={index} className="relative">
              {/* Connection Line */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-16 left-full w-full h-0.5 bg-gradient-to-r from-primary/50 to-transparent z-0" />
              )}

              <Card className="relative z-10 h-full">
                <CardContent className="p-6">
                  <div className="flex items-center justify-center w-12 h-12 bg-primary/20 rounded-full mb-4">
                    <step.icon className="h-6 w-6 text-primary" />
                  </div>

                  <div className="flex items-center gap-2 mb-3">
                    <Badge variant="outline" className="text-xs">
                      Step {index + 1}
                    </Badge>
                  </div>

                  <h3 className="font-semibold text-lg mb-3">{step.title}</h3>
                  <p className="text-sm text-muted-foreground mb-4">{step.description}</p>

                  <ul className="space-y-1">
                    {step.details.map((detail, detailIndex) => (
                      <li key={detailIndex} className="text-xs text-muted-foreground flex items-center gap-2">
                        <div className="w-1 h-1 bg-primary rounded-full" />
                        {detail}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>
          ))}
        </div>

        <div className="mt-16 text-center">
          <Card className="max-w-2xl mx-auto">
            <CardContent className="p-8">
              <h3 className="font-semibold text-xl mb-4">End-to-End Security</h3>
              <p className="text-muted-foreground mb-6">
                The entire process takes less than 2 seconds and provides a confidence score along with detailed
                reasoning for each verification result.
              </p>
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-primary">{"<2s"}</div>
                  <div className="text-sm text-muted-foreground">Processing Time</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-primary">97%+</div>
                  <div className="text-sm text-muted-foreground">Accuracy Rate</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-primary">24/7</div>
                  <div className="text-sm text-muted-foreground">Availability</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  )
}

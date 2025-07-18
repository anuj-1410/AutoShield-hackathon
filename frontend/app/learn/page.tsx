import { Header } from "@/components/layout/header"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Shield, Brain, Lock, Users, Zap, Eye, BookOpen, HelpCircle, FileText } from "lucide-react"

export default function LearnPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Learn About AutoShield</h1>
          <p className="text-muted-foreground">
            Understand how our AI-powered verification system protects Web3 ecosystems
          </p>
        </div>

        <div className="grid gap-8">
          {/* How It Works */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-5 w-5" />
                How AutoShield Works
              </CardTitle>
              <CardDescription>A comprehensive overview of our verification process</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-3">
                <div className="text-center">
                  <div className="w-12 h-12 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Eye className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="font-semibold mb-2">1. Data Collection</h3>
                  <p className="text-sm text-muted-foreground">
                    Our AI analyzes public blockchain data, transaction patterns, and behavioral signals
                  </p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Brain className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="font-semibold mb-2">2. AI Analysis</h3>
                  <p className="text-sm text-muted-foreground">
                    Machine learning models detect patterns indicative of fake accounts and fraud
                  </p>
                </div>
                <div className="text-center">
                  <div className="w-12 h-12 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Shield className="h-6 w-6 text-primary" />
                  </div>
                  <h3 className="font-semibold mb-2">3. Blockchain Verification</h3>
                  <p className="text-sm text-muted-foreground">
                    Results are cryptographically signed and stored on-chain for transparency
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Key Features */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="h-5 w-5" />
                Key Features
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                <div className="flex gap-3">
                  <Shield className="h-5 w-5 text-primary mt-1" />
                  <div>
                    <h4 className="font-semibold">Real-time Verification</h4>
                    <p className="text-sm text-muted-foreground">Instant account verification with 97%+ accuracy</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <Lock className="h-5 w-5 text-primary mt-1" />
                  <div>
                    <h4 className="font-semibold">Privacy Preserving</h4>
                    <p className="text-sm text-muted-foreground">
                      Only verification results stored on-chain, not personal data
                    </p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <Users className="h-5 w-5 text-primary mt-1" />
                  <div>
                    <h4 className="font-semibold">Community Driven</h4>
                    <p className="text-sm text-muted-foreground">
                      Decentralized governance and community feedback integration
                    </p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <Brain className="h-5 w-5 text-primary mt-1" />
                  <div>
                    <h4 className="font-semibold">Adaptive AI</h4>
                    <p className="text-sm text-muted-foreground">
                      Continuously learning and improving detection capabilities
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* FAQ */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <HelpCircle className="h-5 w-5" />
                Frequently Asked Questions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Accordion type="single" collapsible className="w-full">
                <AccordionItem value="item-1">
                  <AccordionTrigger>How accurate is AutoShield's detection?</AccordionTrigger>
                  <AccordionContent>
                    AutoShield achieves 97%+ accuracy in detecting fake accounts through advanced machine learning
                    models trained on millions of blockchain transactions and behavioral patterns. Our system
                    continuously improves through community feedback and model updates.
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="item-2">
                  <AccordionTrigger>What data does AutoShield collect?</AccordionTrigger>
                  <AccordionContent>
                    AutoShield only analyzes publicly available blockchain data including transaction patterns, account
                    age, interaction networks, and on-chain behavior. No personal information or private keys are ever
                    collected or stored.
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="item-3">
                  <AccordionTrigger>How can I integrate AutoShield into my dApp?</AccordionTrigger>
                  <AccordionContent>
                    Integration is simple through our REST API or smart contract calls. Check our developer
                    documentation for code examples and implementation guides. Most integrations can be completed in
                    under 30 minutes.
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="item-4">
                  <AccordionTrigger>What if my account is incorrectly flagged?</AccordionTrigger>
                  <AccordionContent>
                    You can request re-verification through your dashboard. Our team reviews all appeals within 24
                    hours. False positives help improve our system and are taken seriously.
                  </AccordionContent>
                </AccordionItem>

                <AccordionItem value="item-5">
                  <AccordionTrigger>Is AutoShield decentralized?</AccordionTrigger>
                  <AccordionContent>
                    Yes, verification results are stored on-chain for transparency and immutability. While AI processing
                    happens off-chain for efficiency, all results are cryptographically signed and publicly verifiable.
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </CardContent>
          </Card>

          {/* Privacy & Security */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Lock className="h-5 w-5" />
                Privacy & Security
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold mb-2">Data Privacy</h4>
                <p className="text-sm text-muted-foreground mb-3">
                  AutoShield is designed with privacy-first principles:
                </p>
                <ul className="text-sm space-y-1 text-muted-foreground">
                  <li>• Only public blockchain data is analyzed</li>
                  <li>• No personal information is collected or stored</li>
                  <li>• Analysis results are hashed before on-chain storage</li>
                  <li>• Users maintain full control over their data</li>
                </ul>
              </div>

              <div>
                <h4 className="font-semibold mb-2">Security Measures</h4>
                <ul className="text-sm space-y-1 text-muted-foreground">
                  <li>• Cryptographic signatures ensure data integrity</li>
                  <li>• Multi-layer validation prevents manipulation</li>
                  <li>• Regular security audits and updates</li>
                  <li>• Decentralized architecture reduces single points of failure</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Getting Started */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5" />
                Getting Started
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                <div className="border rounded-lg p-4">
                  <h4 className="font-semibold mb-2">For Users</h4>
                  <ol className="text-sm space-y-2 text-muted-foreground">
                    <li>1. Connect your Web3 wallet</li>
                    <li>2. View your verification status</li>
                    <li>3. Download your attestation</li>
                    <li>4. Use verified status across dApps</li>
                  </ol>
                </div>

                <div className="border rounded-lg p-4">
                  <h4 className="font-semibold mb-2">For Developers</h4>
                  <ol className="text-sm space-y-2 text-muted-foreground">
                    <li>1. Review API documentation</li>
                    <li>2. Integrate verification checks</li>
                    <li>3. Test with sample addresses</li>
                    <li>4. Deploy to production</li>
                  </ol>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Resources */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Additional Resources
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-3 md:grid-cols-3">
                <a
                  href="#"
                  className="flex items-center gap-2 p-3 border rounded-lg hover:bg-muted/50 transition-colors"
                >
                  <FileText className="h-4 w-4" />
                  <span className="text-sm">API Documentation</span>
                </a>
                <a
                  href="#"
                  className="flex items-center gap-2 p-3 border rounded-lg hover:bg-muted/50 transition-colors"
                >
                  <BookOpen className="h-4 w-4" />
                  <span className="text-sm">Developer Guide</span>
                </a>
                <a
                  href="#"
                  className="flex items-center gap-2 p-3 border rounded-lg hover:bg-muted/50 transition-colors"
                >
                  <Shield className="h-4 w-4" />
                  <span className="text-sm">Security Whitepaper</span>
                </a>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

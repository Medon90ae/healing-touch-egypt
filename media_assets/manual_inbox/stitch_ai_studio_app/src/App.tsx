/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { Hero } from './components/Hero';
import { StageCalculator } from './components/StageCalculator';
import { ProtocolKits } from './components/ProtocolKits';
import { ClinicalComparison } from './components/ClinicalComparison';
import { ShowerGuide } from './components/ShowerGuide';
import { ReviewsAndFAQ } from './components/ReviewsAndFAQ';
import { CheckoutDrawer } from './components/CheckoutDrawer';
import { OrderLookupModal } from './components/OrderLookupModal';
import { MobileStickyBar } from './components/MobileStickyBar';
import { Footer } from './components/Footer';
import { CartItem, Order } from './types/protocol';
import { PROTOCOL_PRODUCTS } from './data/protocolData';
import { CheckCircle2 } from 'lucide-react';

export default function App() {
  // Cart State (Initialized with default complete bundle for high-conversion seamless start)
  const [cart, setCart] = useState<CartItem[]>(() => {
    const saved = localStorage.getItem('healing_touch_cart');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        // fallback
      }
    }
    const bundle = PROTOCOL_PRODUCTS.find((p) => p.id === 'complete-protocol-bundle')!;
    return [{ product: bundle, quantity: 1 }];
  });

  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false);
  const [isOrdersOpen, setIsOrdersOpen] = useState(false);
  const [orders, setOrders] = useState<Order[]>([]);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Sync cart to localStorage
  useEffect(() => {
    localStorage.setItem('healing_touch_cart', JSON.stringify(cart));
  }, [cart]);

  // Load orders from localStorage
  useEffect(() => {
    const savedOrders = localStorage.getItem('healing_touch_orders');
    if (savedOrders) {
      try {
        setOrders(JSON.parse(savedOrders));
      } catch {
        // ignore
      }
    }
  }, []);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 3000);
  };

  const handleAddToCart = (productId: string) => {
    const product = PROTOCOL_PRODUCTS.find((p) => p.id === productId);
    if (!product) return;

    setCart((prev) => {
      const existing = prev.find((item) => item.product.id === productId);
      if (existing) {
        return prev.map((item) =>
          item.product.id === productId
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prev, { product, quantity: 1 }];
    });

    showToast(`تمت إضافة "${product.titleAr}" إلى سلة مشترياتك`);
  };

  const handleInstantBuy = (productId: string) => {
    const product = PROTOCOL_PRODUCTS.find((p) => p.id === productId);
    if (!product) return;

    setCart((prev) => {
      const exists = prev.some((item) => item.product.id === productId);
      if (exists) return prev;
      return [...prev, { product, quantity: 1 }];
    });

    setIsCheckoutOpen(true);
  };

  const handleUpdateQuantity = (productId: string, quantity: number) => {
    setCart((prev) =>
      prev.map((item) =>
        item.product.id === productId ? { ...item, quantity } : item
      )
    );
  };

  const handleRemoveItem = (productId: string) => {
    setCart((prev) => prev.filter((item) => item.product.id !== productId));
  };

  const handleClearCart = () => {
    setCart([]);
  };

  const handleOrderPlaced = (newOrder: Order) => {
    setOrders((prev) => [newOrder, ...prev]);
    showToast(`تم تسجيل طلبك بنجاح برقم: ${newOrder.orderNumber}`);
  };

  const scrollToSection = (sectionId: string) => {
    const el = document.getElementById(sectionId);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const totalCartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <div className="min-h-screen bg-[#fbfdfb] text-[#121c2a] flex flex-col font-sans selection:bg-[#059669]/20 selection:text-[#064e3b]">
      
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed top-20 left-1/2 -translate-x-1/2 z-50 bg-[#064e3b] text-white px-5 py-2.5 rounded-full shadow-lg text-xs font-semibold flex items-center gap-2 border border-[#82f5c1]/30 animate-in fade-in slide-in-from-top-4 duration-200">
          <CheckCircle2 className="w-4 h-4 text-[#82f5c1] shrink-0" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Top Bar Header */}
      <Header
        cartCount={totalCartCount}
        onOpenCart={() => setIsCheckoutOpen(true)}
        onOpenOrders={() => setIsOrdersOpen(true)}
        onScrollTo={scrollToSection}
      />

      {/* Main Content Sections */}
      <main className="flex-1">
        {/* Hero Section */}
        <Hero
          onStartCalculator={() => scrollToSection('calculator')}
          onExploreProtocol={() => scrollToSection('products')}
          onInstantOrder={() => handleInstantBuy('complete-protocol-bundle')}
        />

        {/* Interactive Recovery Stage & Shower Readiness Calculator */}
        <StageCalculator
          onSelectProduct={(id) => handleInstantBuy(id)}
          onAddToCart={handleAddToCart}
        />

        {/* 3-Phase Protocol Kits & Products */}
        <ProtocolKits
          onAddToCart={handleAddToCart}
          onInstantBuy={handleInstantBuy}
        />

        {/* Clinical Comparison with Ordinary Bandages */}
        <ClinicalComparison />

        {/* Step-by-Step Safe Shower Guide */}
        <ShowerGuide />

        {/* Mother Experiences & Clinical FAQ */}
        <ReviewsAndFAQ />
      </main>

      {/* Footer */}
      <Footer
        onScrollTo={scrollToSection}
        onOpenOrders={() => setIsOrdersOpen(true)}
      />

      {/* Mobile Sticky Conversion Drawer (under 15% viewport height) */}
      <MobileStickyBar
        cartCount={totalCartCount}
        onOpenCheckout={() => setIsCheckoutOpen(true)}
      />

      {/* Slide-over Checkout Drawer (COD & InstaPay for Egypt) */}
      <CheckoutDrawer
        isOpen={isCheckoutOpen}
        onClose={() => setIsCheckoutOpen(false)}
        cart={cart}
        onUpdateQuantity={handleUpdateQuantity}
        onRemoveItem={handleRemoveItem}
        onClearCart={handleClearCart}
        onOrderPlaced={handleOrderPlaced}
      />

      {/* Order Lookup & Shipping Tracker Modal */}
      <OrderLookupModal
        isOpen={isOrdersOpen}
        onClose={() => setIsOrdersOpen(false)}
        orders={orders}
      />

    </div>
  );
}

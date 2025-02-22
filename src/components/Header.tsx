"use client";

import { useBasic, useQuery } from "@basictech/react";
import { Instagram, Search, Heart, PlusSquare, User } from "lucide-react";

import { BrowserAI } from "@browserai/browserai";

const browserAI = new BrowserAI();


export default function Header() {
    const { db } = useBasic();
   
    const { signin, isSignedIn, user, signout } = useBasic();

    return (
        <header className="header">
            <div className="header-container">
                <div className="header-logo">
                    <Instagram className="w-8 h-8" />
                    <h1>The Daily Chew</h1>
                </div>

                <div className="header-search">
                    <Search className="w-4 h-4" />
                    <input type="text" placeholder="Search" />
                </div>

                <nav className="header-nav">
                    <button>
                        <PlusSquare className="w-6 h-6" />
                    </button>
                    <button>
                        <Heart className="w-6 h-6" />
                    </button>
                    <button>
                        <div>
                            {isSignedIn ? (
                                <div>
                                    <p>Signed in as: {user.email}</p>
                                    {/* Add a button to sign out */}
                                    <button onClick={signout}>Sign Out</button>
                                </div>
                            ) : (
                                <button onClick={signin}><User className="w-6 h-6" /></button>
                            )}
                        </div>

                    </button>
                </nav>
            </div>
        </header>
    );
}

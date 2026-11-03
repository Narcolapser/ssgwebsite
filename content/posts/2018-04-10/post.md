I'm embarking on a route that scares me a little. This blog post is mostly me thinking out loud and trying to come to grips with it.

#Past

I started a library back in 2015 for interacting with Office 365 via Python. It has done very very well for itself. It was the first real library I ever made. I made it simple to access people's inboxes, calendars, and contacts In Office 365 in their python scripts. I meant it primarily as a tool for writing server-side scripts. Specifically, I was using it for things like providing Lifehope staff the ability to print by emailing a PDF. If you've ever worked as a sysadmin, you are probably familiar with the endless problems of people trying to print; Such fickle machines and protocols. I also created it for querying the system for vehicle availability of the Lifehope pool vehicles. It worked great, and I was pleased with the library I made.

Boldly I put it out on the internet, in PyPI, and let the world see and enjoy. In those days PyPI still gave download counts, and I saw that I was getting a couple of hundred downloads. In the first few weeks of it, I think I peeked at 1,000 views on GitHub and like 8 stars. I felt like I had contributed to the community for the first time.

#Present

After I left Lifehope, I no longer had an Office 365 account, so I could no longer work on the library. So I marked it as not under active development, and it sat on a shelf for a year and a half. About a year ago though I got an Office 365 account from the University of South Dakota, so I could work on it again. However, there is nothing at USD that uses it, so I mostly fiddled with it in my free time or during the odd moments when I needed to write a script for something USD needed.

Without any aid from myself though, the library kept growing in popularity. As of writing, it has 145 stars, 21 contributors, and sees about 1,500 views per week. Once or twice a month, people open an issue and start or finish it with a comment about it being "a great library!" or "it helped me a lot!" O365 is an excellent tool for many people, and I'm very proud of it. Again, I felt like I contributed to the community.

#Future

However, now comes the hard part. A few months ago, a fellow named @Roycem90 submitted a new pair of classes, the Fluent classes, that simplified the usage of the library significantly. I was reluctant at first as it was far from an elegant way of doing it, but I liked the idea he was going after. So I merged it in. I started thinking about how to make the library more pythonic. There were much get and set statement strewn about making it feel more like a java library than a python library. There were also some oddities with accessing calendars because of the way the API that underpinned the library worked. At the same time, I created a branch that demonstrated some of the new ways I wanted to go about this @Janscas informed me of his fork. He started with a total rewrite of the library. It was way more in line with what I was thinking than the current library. After a [long](https://github.com/Narcolapser/python-o365/commit/78e5a5aa0e3b7de1c3d1fc1054e5e753e34db9a4) discussion, we decided to stick with the new code base @Janscas had created and made it version 2 of the library.

I set up a GitHub organization, [O365](https://github.com/O365) and started the process of setting up the project there. That's when I ran into a small personal crisis. If I go down this road, O365 is going to grow beyond me. By the time we the rewrite is complete, @Janscas will have more lines of code in the library than I will. (That may not be true if you factor in tests, but the actual code that runs on people's machines would primarily not be mine.) The success of this project stroked my ego, so did how good it looks in my portfolio; I don't want just to let that go.

It's not easy, but I think I'm going to have to. I want to hold on to that posterity. However, the conclusion I've come to is I want O365 to thrive, even if I'm not the maintainer. From a pragmatic point of view, if I don't do this, @janscas will recreate the library, and everyone will eventually switch to that, resigning O365 to the history books so to speak. Which I guess is the part of this that's a little hard. I wanted, of course, people to contribute code, but now @Janscas has contributed so much it's grown beyond me. Whatever I do, I lose O365.

However, the final thing that hit me was this: I don't actually like maintaining O365. I don't use it anymore. Had I stayed on at life hope I probably would have found many more uses for the library, scripting all sorts of things. However, as it stands, I'm programming professionally in Java, so O365 is worthless, at home I don't do anything with Office 365, so O365 is worthless. As much as I love this little library of mine, I'm not actually in an excellent position to maintain it.

#Conclusion

It's time for O365 to grow up and beyond me. Maybe @janscas will take over as the maintainer. For now, I still "own" the organization O365 and will be helping in the project's guidance. But the day may come where I step down as a maintainer of O365 and let that project soar on its own.


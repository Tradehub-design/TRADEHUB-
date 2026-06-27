import streamlit as st

from engine.screenshot_link_engine import ScreenshotLinkEngine


class ScreenshotTimeline:

    @staticmethod
    def render(screenshots):
        if screenshots is None or screenshots.empty:
            st.info("No screenshots linked to this trade yet.")
            return

        order = ScreenshotLinkEngine.timeline_order()

        for screenshot_type in order:
            group = screenshots[
                screenshots["screenshot_type"] == screenshot_type
            ] if "screenshot_type" in screenshots.columns else screenshots.iloc[0:0]

            if group.empty:
                continue

            with st.expander(
                f"{screenshot_type} ({len(group)})",
                expanded=True
            ):
                for _, shot in group.iterrows():
                    url = shot.get("public_url")

                    if url:
                        st.image(
                            url,
                            use_container_width=True
                        )

                    notes = shot.get("notes")

                    if notes:
                        st.info(notes)

                    created_at = shot.get("created_at")

                    if created_at:
                        st.caption(created_at)

        unknown = screenshots[
            ~screenshots["screenshot_type"].isin(order)
        ] if "screenshot_type" in screenshots.columns else screenshots

        if not unknown.empty:
            with st.expander(
                f"Other ({len(unknown)})",
                expanded=False
            ):
                for _, shot in unknown.iterrows():
                    url = shot.get("public_url")

                    if url:
                        st.image(
                            url,
                            use_container_width=True
                        )

                    if shot.get("notes"):
                        st.info(shot.get("notes"))

"""
HTS Dashboard - Hierarchy Visualization Component

This module provides interactive visualization of the HTS code hierarchy
using Plotly for tree diagrams and navigation.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import List, Dict


def create_hierarchy_tree(codes: List[Dict[str, str]]) -> go.Figure:
    """
    Create an interactive tree diagram of HTS hierarchy.
    
    Args:
        codes: List of dictionaries with 'hts_code', 'title', and optional 'count'
    
    Returns:
        Plotly Figure object
    """
    
    # Build hierarchy structure
    hierarchy = {}
    
    for code_data in codes:
        code = code_data.get('hts_code', '')
        title = code_data.get('title', 'Untitled')
        
        # Extract hierarchy levels
        if len(code) >= 2:
            chapter = code[:2]
            if chapter not in hierarchy:
                hierarchy[chapter] = {
                    'title': f"Chapter {chapter}",
                    'children': {}
                }
            
            if len(code) >= 4:
                heading = code[:4]
                if heading not in hierarchy[chapter]['children']:
                    hierarchy[chapter]['children'][heading] = {
                        'title': title[:40],
                        'children': []
                    }
                
                if len(code) > 4:
                    hierarchy[chapter]['children'][heading]['children'].append({
                        'code': code,
                        'title': title
                    })
    
    # Create tree diagram using Plotly
    labels = []
    parents = []
    values = []
    colors = []
    
    # Color palette for chapters
    chapter_colors = [
        '#4cc9f0', '#7209b7', '#f72585', '#06ffa5', '#ffd60a',
        '#ef476f', '#4cc9f0', '#7209b7', '#f72585', '#06ffa5'
    ]
    
    # Root node
    labels.append("HTS Codes")
    parents.append("")
    values.append(len(codes))
    colors.append('#161b22')
    
    # Add chapters
    for idx, (chapter, chapter_data) in enumerate(hierarchy.items()):
        labels.append(f"{chapter}: {chapter_data['title']}")
        parents.append("HTS Codes")
        values.append(len(chapter_data['children']))
        colors.append(chapter_colors[idx % len(chapter_colors)])
        
        # Add headings
        for heading, heading_data in chapter_data['children'].items():
            labels.append(f"{heading}: {heading_data['title']}")
            parents.append(f"{chapter}: {chapter_data['title']}")
            values.append(len(heading_data['children']) if heading_data['children'] else 1)
            colors.append(chapter_colors[idx % len(chapter_colors)])
    
    # Create sunburst chart
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(
            colors=colors,
            line=dict(color='#0d1117', width=2)
        ),
        hovertemplate='<b>%{label}</b><br>Items: %{value}<extra></extra>',
        textfont=dict(size=12, color='white'),
    ))
    
    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
    )
    
    return fig


def render_breadcrumb(path: List[str]) -> None:
    """
    Render a breadcrumb navigation trail.
    
    Args:
        path: List of hierarchy levels (e.g., ['Chapter 39', 'Heading 3923', 'Code 3923.30'])
    """
    
    breadcrumb_html = '<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 20px;">'
    
    for i, item in enumerate(path):
        if i > 0:
            breadcrumb_html += '<span style="color: rgba(255, 255, 255, 0.4);">→</span>'
        
        breadcrumb_html += f'''
            <span style="
                padding: 6px 12px;
                background: rgba(76, 201, 240, 0.15);
                border: 1px solid rgba(76, 201, 240, 0.3);
                border-radius: 6px;
                color: var(--accent-blue);
                font-size: 13px;
                font-weight: 600;
            ">{item}</span>
        '''
    
    breadcrumb_html += '</div>'
    
    st.markdown(breadcrumb_html, unsafe_allow_html=True)


def hierarchy_explorer(codes: List[Dict[str, str]]) -> None:
    """
    Render an interactive hierarchy explorer with visualization.
    
    Args:
        codes: List of HTS codes with metadata
    """
    
    st.markdown('<h3 class="section-title" style="font-size: 24px;">🌳 HTS Hierarchy Visualization</h3>', unsafe_allow_html=True)
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 Sunburst Chart", "📋 Tree View"])
    
    with tab1:
        st.markdown(
            '<p class="subtitle">Interactive sunburst chart showing HTS code hierarchy. Click segments to zoom in.</p>',
            unsafe_allow_html=True
        )
        
        fig = create_hierarchy_tree(codes)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 Click on any segment to zoom in. Click the center to zoom out.")
    
    with tab2:
        st.markdown(
            '<p class="subtitle">Expandable tree view of HTS codes organized by chapter and heading.</p>',
            unsafe_allow_html=True
        )
        
        # Group codes by chapter
        chapters = {}
        for code_data in codes:
            code = code_data.get('hts_code', '')
            if len(code) >= 2:
                chapter = code[:2]
                if chapter not in chapters:
                    chapters[chapter] = []
                chapters[chapter].append(code_data)
        
        # Display as expandable tree
        for chapter, chapter_codes in sorted(chapters.items()):
            with st.expander(f"📁 Chapter {chapter} ({len(chapter_codes)} codes)", expanded=False):
                for code_data in chapter_codes[:10]:  # Limit to first 10 for performance
                    st.markdown(
                        f"""
                        <div class="glass-card" style="padding: 12px; margin-bottom: 8px;">
                            <strong style="color: var(--accent-blue);">{code_data.get('hts_code')}</strong>
                            <p style="margin: 4px 0 0 0; font-size: 14px; color: rgba(255, 255, 255, 0.8);">
                                {code_data.get('title', 'No title')[:100]}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                if len(chapter_codes) > 10:
                    st.info(f"... and {len(chapter_codes) - 10} more codes in this chapter")

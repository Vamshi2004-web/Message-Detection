/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package servlet;

import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 *
 * @author DELL
 */
@WebServlet(name = "report", urlPatterns = {"/report"})
public class report extends HttpServlet {

    /**
     * Processes requests for both HTTP <code>GET</code> and <code>POST</code>
     * methods.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    protected void processRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        try (PrintWriter out = response.getWriter()) {
            /* TODO output your page here. You may use following sample code. */
            out.println("<!DOCTYPE html>");
            out.println("<html>");
            out.println("<head>");
            out.println("<title>Servlet report</title>");            
            out.println("</head>");
            out.println("<body>");
            out.println("<h1>Servlet report at " + request.getContextPath() + "</h1>");
            out.println("</body>");
            out.println("</html>");
        }
    }

    // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
    /**
     * Handles the HTTP <code>GET</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        processRequest(request, response);
    }

    /**
     * Handles the HTTP <code>POST</code> method.
     *
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        PrintWriter out = response.getWriter();
        Connection con = null;
        PreparedStatement pstmt = null;
        String n = "", p = "", x = "", y = "", z = "", t = "";

        // Get parameters from the request
        n = request.getParameter("customer-name");
        x = request.getParameter("contact-info");
        p = request.getParameter("problem-description");
        y = request.getParameter("steps-taken");
        z = request.getParameter("current-status");
        t = request.getParameter("resolution-plan");

        try {
            // Load the Apache Derby JDBC driver
            Class.forName("org.apache.derby.jdbc.ClientDriver");

            // Establish connection to the Derby database using the updated URL and credentials
            con = DriverManager.getConnection("jdbc:derby://localhost:1527/user", "root", "root");

            // SQL query for inserting data into the 'report' table
            String sql = "INSERT INTO report(customername, contactinfo, problemdescription, stepstaken, currentstatus, resolutionplan) VALUES (?, ?, ?, ?, ?, ?)";
            pstmt = con.prepareStatement(sql);
            pstmt.setString(1, n);
            pstmt.setString(2, x);
            pstmt.setString(3, p);
            pstmt.setString(4, y);
            pstmt.setString(5, z);
            pstmt.setString(6, t);

            // Execute the insert query
            pstmt.executeUpdate();

            // Forward the request to the dashboard page after successful insertion
            RequestDispatcher rd = request.getRequestDispatcher("dashboard.html");
            rd.forward(request, response);
        } catch (Exception e) {
            // If there is an exception, display the error message
            out.println("<font color=red size=24>Report submission failed!!<br>");
            out.println("<a href='registration.html'>Go back</a>");
        } finally {
            try {
                // Close all resources to avoid memory leaks
                if (pstmt != null) {
                    pstmt.close();
                }
                if (con != null) {
                    con.close();
                }
                if (out != null) {
                    out.close();
                }
            } catch (SQLException ex) {
                out.println("Error in closing resources: " + ex.getMessage());
            }
        }
    }
    /**
     * Returns a short description of the servlet.
     *
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "Short description";
    }// </editor-fold>

}
